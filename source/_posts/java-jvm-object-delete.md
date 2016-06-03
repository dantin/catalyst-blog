title: 深入理解Java虚拟机之三：对象的回收判断及死亡过程
date: 2016-06-04 00:27:14
categories: 学术
tags: [Java, JVM]
toc: true
---

JVM的堆里存放着几乎所有的对象实例，垃圾收集器要进行垃圾回收，首先要做就是找出哪些对象是需要回收的。

### 对象的回收判断

常用的判断方法有两种。

#### 引用计数算法

__Reference Counting__

为每一个对象添加一个引用计数器，每当有其他对象持有对它的引用时，该计数器加1。这种算法实现简单，判断效率高，是一个很不错的算法，Python、COM和Squirrel中都用它来管理内存。但主流的Java虚拟机实现中并没有使用这个算法，主要原因是：它很难解决对象之间的循环引用问题。

比如：在对象A中持有一个指向B的成员，而在对象B中又有一个指向A的成员，那么这两个对象将无法被回收，造成了内存泄露。

#### 可达性分析算法

通过一系列的称为“GC Roots的对象作为起始点，从这些节点开始向下搜索，搜索所走过的路径称为引用链（Reference Chain）。当一个对象从GC Roots不可达时，则证明这个对象时应该被回收的。这样，即使对象A和B之间有互有引用，但如果GC Roots不可达，它们还是会被垃圾回收器回收。

![可达性分析算法](/images/jvm-gc-root.jpg "GC root")

Java中可作为GC Root的对象有：

1. 虚拟机栈(Java Stack)中引用的对象（本地变量表）；
2. 方法区中静态属性引用的对象；
3. 方法区中常量引用的对象；
4. 本地方法栈中JNI引用的对象（Native对象）。

这两种算法判断都是通过引用贯穿其中。JDK 1.2之后，Java对引用的概念进行了扩充，分为4类：

> 强引用（Strong Reference）、软引用（Soft Reference）、弱引用（Weak Reference）、虚引用（Phantom Reference）。

* 普通代码中默认的都是强引用，例如`Object obj = new Object()`。只要引用还在，永远不会回收。
* 软引用描述一些非必须的对象，只有当内存将要发生OOM前才会将其回收。使用`SoftReference`类来实现。
* 弱引用也用来描述非必须的对象，但是只能生存到下一次垃圾收集发生之前。使用`WeakReference`类来实现。
* 虚引用也成为幽灵引用，它的存在不会影响一个对象的生存时间，也无法通过虚引用获取一个对象实例。它的存在只是为了能在这个对象被收集器回收时能获得系统通知。使用`PhantomReference`类实现。

### 对象的死亡过程

通过引用计数或可达性分析确定一个对象可被回收到该对象死亡要经过两次标记过程：

#### 第一次标记

当第一次被标记为不可达时，它将会进行一次筛选，筛选条件是此对象是否有必要执行finalize()方法。

访对象没有覆盖finalize()或已经被调用过，则虚拟机认为它“没必要执行”。

如果这个对象被判定为有必要执行finalize()方法，则会将这个对象放置在F-Queue的队列之中，并在稍后一个由虚拟机自动建立、低优先级的Finalizer线程去执行它。

__注意__：这里的“执行”仅代表虚拟机会触发这个方法，并不一定会等待它运行结束。防止由于finalize()方法执行缓慢或者发生死循环等导致其它对象处于等待状态。finalize()方法是对象逃脱死亡厄运最后的机会，可以通过将this指针赋值给某个类变量或者对象的成员变量来拯救自己。

#### 第二次标记

触发finalize()方法之后，稍后GC将对F-Queue中的对象进行第二次小规模标记。

如果对象在finalize()中成功拯救了自己，则它将会被移除出“即将回收”的集合。否则之后它就真的被回收了。

finalize()方法并不建议使用，因为它运行代价高昂，不确定性太大，而且不能保证各个对象之间的调用顺序。

### 方法区的垃圾回收

Java虚拟机规范中并没有强制要求虚拟机必须实现方法区（HotSpot中的永久代）的垃圾回收，而且方法区中进行垃圾收集的“性价比”比较低：在堆中，尤其是新生代中，常规应用进行一次垃圾收集一般可以回收70%~95%的空间，而永久代的垃圾收集效率远低于此。

方法区中垃圾收集主要分为两部分：_废弃常量_和_无用的类_

* 废弃常量回收与Java堆中对象的收集非常类似。如果没有任何地方引用这些常量便会被系统清理。

* 无用的类的回收就比较复杂。只有该类满足下面三个条件才算是“无用的类”：
                
    1. 该类的所有实例都已经被回收
    2. 加载该类的ClassLoader已经被回收了
    3. 该类对应的java.lang.Class对象没有在被任何地方被引用，无法再任何地方通过反射访问该类的方法

当然满足了这3个条件，并不是一定会回收。HotSpot提供了-Xnoclassgc参数来控制。

`-Xnoclassgc`每次永久存储区满了后一般GC算法在做扩展分配内存前都会触发一次Full GC，除非设置了-Xnoclassgc。

在大量使用反射、动态代理、CGLib等ByteCode框架、动态生成JSP以及OSGi这类频繁自定义ClassLoader的场景都需要虚拟机具备类卸载功能。

### 演示代码

#### 拯救示例

此代码演示了两点： 

1. 对象可以在被GC时自我拯救
2. 这种自救的机会只有一次，因为一个对象的finalize()方法最多只会被系统自动调用一次

```java
public class FinalizeEscapeGC {

    public static FinalizeEscapeGC SAVE_HOOK = null;

    public void isAlive() {
        System.out.println("yes, i am still alive :)");
    }

    @Override
    protected void finalize() throws Throwable {
        super.finalize();
        System.out.println("finalize mehtod executed!");
        FinalizeEscapeGC.SAVE_HOOK = this;
    }

    public static void main(String[] args) throws Throwable {
        SAVE_HOOK = new FinalizeEscapeGC();

        //对象第一次成功拯救自己
        SAVE_HOOK = null;
        System.gc();
        // 因为Finalizer方法优先级很低，暂停0.5秒，以等待它。
        // 防止finalize虽然被触发但是没有执行完成。
        //
        // 注释掉sleep方法后，会出现finalize没有执行完而程序就退出的情况
        Thread.sleep(500);
        if (SAVE_HOOK != null) {
            SAVE_HOOK.isAlive();
        } else {
            System.out.println("no, i am dead :(");
        }
    }
}
```