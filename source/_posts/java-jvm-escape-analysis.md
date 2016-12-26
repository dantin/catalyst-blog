---
title: Java中的逃逸分析和TLAB以及Java对象分配
date: 2016-08-03 18:40:40
categories: 学术
tags: [Java, JVM]
toc: true
---

在学习使用Java的过程中，一般认为new出来的对象都是被分配在堆上，但是这个结论不是那么的绝对，通过对Java对象分配的过程分析，可以知道有两个地方会导致Java中new出来的对象并非一定分配在所认为的堆上。这两个点分别是Java中的逃逸分析和TLAB（Thread Local Allocation Buffer）。

### 逃逸分析

#### 逃逸分析的定义

逃逸分析，是一种可以有效减少Java 程序中同步负载和内存堆分配压力的跨函数全局数据流分析算法。通过逃逸分析，Java Hotspot编译器能够分析出一个新的对象的引用的使用范围从而决定是否要将这个对象分配到堆上。

在计算机语言编译器优化原理中，逃逸分析是指分析指针动态范围的方法，它同编译器优化原理的指针分析和外形分析相关联。当变量（或者对象）在方法中分配后，其指针有可能被返回或者被全局引用，这样就会被其他过程或者线程所引用，这种现象称作指针（或者引用）的逃逸(Escape)。

Java在Java SE 6u23以及以后的版本中支持并默认开启了逃逸分析的选项。Java的 HotSpot JIT编译器，能够在方法重载或者动态加载代码的时候对代码进行逃逸分析，同时Java对象在堆上分配和内置线程的特点使得逃逸分析成Java的重要功能。

#### 逃逸分析的方法

Java Hotspot编译器使用的是Jong-Deok Choi, Manish Gupta, Mauricio Seffano,Vugranam C. Sreedhar, Sam Midkiff等在论文《Escape Analysis for Java》中描述的算法进行逃逸分析的。该算法引入了连通图，用连通图来构建对象和对象引用之间的可达性关系，并在此基础上，提出一种组合数据流分析法。由于算法是上下文相关和流敏感的，并且模拟了对象任意层次的嵌套关系，所以分析精度较高，只是运行时间和内存消耗相对较大。

绝大多数逃逸分析的实现都基于一个所谓“封闭世界(closed world)”的前提：所有可能被执行的，方法在做逃逸分析前都已经得知，并且，程序的实际运行不会改变它们之间的调用关系 。但当真实的Java程序运行时，这样的假设并不成立。Java程序拥有的许多特性，例如动态类加载、调用本地函数以及反射程序调用等等，都将打破所谓“封闭世界”的约定。

不管是在“封闭世界”还是在“开放世界”，逃逸分析，作为一种算法而非编程语言的存在，吸引了国内外大量的学者对其进行研究。参见：[谷歌学术搜索](http://www.gfsoso.com/scholar?q=Escape%20Analysis)。

#### 逃逸分析后的处理

经过逃逸分析之后，可以得到三种对象的逃逸状态。

* GlobalEscape（全局逃逸）， 即一个对象的引用逃出了方法或者线程。例如，一个对象的引用是复制给了一个类变量，或者存储在在一个已经逃逸的对象当中，或者这个对象的引用作为方法的返回值返回给了调用方法。
* ArgEscape（参数级逃逸），即在方法调用过程当中传递对象的应用给一个方法。这种状态可以通过分析被调方法的二进制代码确定。
* NoEscape（没有逃逸），一个可以进行标量替换的对象。可以不将这种对象分配在传统的堆上。

编译器可以使用逃逸分析的结果，对程序进行一下优化。
* 堆分配对象变成栈分配对象。一个方法当中的对象，对象的引用没有发生逃逸，那么这个方法可能会被分配在栈内存上而非常见的堆内存上。
* 消除同步。线程同步的代价是相当高的，同步的后果是降低并发性和性能。逃逸分析可以判断出某个对象是否始终只被一个线程访问，如果只被一个线程访问，那么对该对象的同步操作就可以转化成没有同步保护的操作，这样就能大大提高并发程度和性能。
* 矢量替代。逃逸分析方法如果发现对象的内存存储结构不需要连续进行的话，就可以将对象的部分甚至全部都保存在CPU寄存器内，这样能大大提高访问速度。

下面，我们看一下逃逸分析的例子。

```java
public class Main {
    public static void main(String[] args) {
        example();
    }

    public static void example() {
        Foo foo = new Foo(); //alloc
        Bar bar = new Bar(); //alloc
        bar.setFoo(foo);
    }
}

class Foo {}

class Bar {
    private Foo foo;
    public void setFoo(Foo foo) {
        this.foo = foo;
    }
}
```

#### 编译器经过逃逸分析的效果

测试代码：

```java
public class EscapeAnalysis {

    private static class Foo {
        private int x;
        private static int counter;

        public Foo() {
            x = (++counter);
        }
    }

    public static void main(String[] args) {
        long start = System.nanoTime();
        for (int i = 0; i < 1000 * 1000 * 10; ++i) {
            Foo foo = new Foo();
        }
        long end = System.nanoTime();
        System.out.println("Time cost is " + (end - start));
    }
}
```

设置Idea JVM运行参数：

```bash
VM options: -server -verbose:gc
```

未开启逃逸分析设置为：

```bash
-server -verbose:gc -XX:-DoEscapeAnalysis
```

未开启逃逸分析的状况下，运行情况如下：

```bash
[GC (Allocation Failure)  33280K->893K(125952K), 0.0014987 secs]
[GC (Allocation Failure)  34173K->709K(125952K), 0.0011690 secs]
[GC (Allocation Failure)  33989K->693K(125952K), 0.0006355 secs]
[GC (Allocation Failure)  33973K->637K(159232K), 0.0011586 secs]
Time cost is 72647329
```

开启逃逸分析设置为：

```bash
-server -verbose:gc -XX:+DoEscapeAnalysis
```

开启逃逸分析的状况下，运行情况如下：

```bash
Time cost is 9913945
```

未开启逃逸分析时，运行上诉代码，JVM执行了GC操作，而在开启逃逸分析情况下，JVM并没有执行GC操作。同时，操作时间上，开启逃逸分析的程序运行时间是未开启逃逸分析时间的13%。

### TLAB

JVM在内存新生代Eden Space中开辟了一小块线程私有的区域，称作TLAB（Thread-local allocation buffer）。默认设定为占用Eden Space的1%。在Java程序中很多对象都是小对象且用过即丢，它们不存在线程共享也适合被快速GC，所以对于小对象通常JVM会优先分配在TLAB上，并且TLAB上的分配由于是线程私有所以没有锁开销。因此在实践中分配多个小对象的效率通常比分配一个大对象的效率要高。

也就是说，Java中每个线程都会有自己的缓冲区称作TLAB（Thread-local allocation buffer），每个TLAB都只有一个线程可以操作，TLAB结合bump-the-pointer技术可以实现快速的对象分配，而不需要任何的锁进行同步，也就是说，在对象分配的时候不用锁住整个堆，而只需要在自己的缓冲区分配即可。

关于对象分配的JDK源码可以参见[JVM 之 Java对象创建和初始化](http://blog.hesey.net/2011/07/object-allocation-on-non-heap.html)中对OpenJDK源码的分析。

### Java对象分配的过程

1. 编译器通过逃逸分析，确定对象是在栈上分配还是在堆上分配。如果是在堆上分配，则进入选项2.
2. 如果tlab_top + size <= tlab_end，则在在TLAB上直接分配对象并增加tlab_top的值，如果现有的TLAB不足以存放当前对象则3.
3. 重新申请一个TLAB，并再次尝试存放当前对象。如果放不下，则4.
4. 在Eden区加锁（这个区是多线程共享的），如果eden_top + size <= eden_end则将对象存放在Eden区，增加eden_top 的值，如果Eden区不足以存放，则5.
5. 执行一次Young GC（minor collection）。
6. 经过Young GC之后，如果Eden区任然不足以存放当前对象，则直接分配到老年代。

对象不在堆上分配主要的原因还是堆是共享的，在堆上分配有锁的开销。无论是TLAB还是栈都是线程私有的，私有即避免了竞争（当然也可能产生额外的问题例如可见性问题），这是典型的用空间换效率的做法。

参考

[对象都是在堆上分配的吗？](http://blog.hesey.net/2011/07/object-allocation-on-non-heap.html)
[JVM 之 Java对象创建和初始化](http://blog.zarue.com/blog/2014/06/15/java-object-create-2/)
[In what cases is Java slower than C++ by a big margin?](http://www.quora.com/In-what-cases-is-Java-slower-than-C-by-a-big-margin)
[Size of Huge Objects directly allocated to Old Generation](http://stackoverflow.com/questions/24618467/size-of-huge-objects-directly-allocated-to-old-generation/24620205#24620205)
[Escape analysis in Java](http://stackoverflow.com/questions/771430/escape-analysis-in-java)
[Escape Analysis](http://docs.oracle.com/javase/7/docs/technotes/guides/vm/performance-enhancements-7.html#escapeAnalysis)
[原文](http://blog.csdn.net/yangzl2008/article/details/43202969)
