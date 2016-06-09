title: Java单例模式
date: 2016-06-09 22:43:47
categories: 工程
tags: Java
toc: true
---

什么是单例模式呢？就是在整个系统中，只有一个唯一存在的实例。

使用Singleton的好处还在于可以节省内存，因为它限制了实例的个数，有利于Java垃圾回收。

### 特点

单例模式主要有3个特点：

1. 单例类确保自己只有一个实例。
2. 单例类必须自己创建自己的实例。
3. 单例类必须为其他对象提供唯一的实例。

### 实现方式

单例模式的实现方式有五种方法：懒汉，恶汉，双重校验锁，枚举和静态内部类。

#### 懒汉模式

```java
public class Singleton {
    private static Singleton instance;
    private Singleton (){}

    public static synchronized Singleton getInstance() {
        if (instance == null) {
            instance = new Singleton();
        }
        return instance;
    }
}
```

这种写法能够在多线程中很好的工作，而且看起来它也具备很好的Lazy Loading，但是，遗憾的是，效率很低，99%情况下不需要同步。

#### 恶汉模式

```java
public class Singleton {
    private static Singleton instance = new Singleton();
    private Singleton (){}

    public static Singleton getInstance() {
        return instance;
    }
}
```

这种方式基于classloder机制避免了多线程的同步问题，但是没有达到Lazy Loading的效果。

#### 双重检测

```java
public class Singleton {
    public static final Singleton singleton = null;
    private Singleton(){}
    public static Singleton getInstance(){
        if(singleton == null){ //如果singleton为空，表明未实例化
           synchronize (Singleton.class){
               if( singleton == null ) { // double check 进来判断后再实例化。
                   singleton = new Singleton();
               }
        }
        return singleton;
    }
}
```

当两个线程执行完第一个 singleton == null 后等待锁， 其中一个线程获得锁并进入synchronize后，实例化了，然后退出释放锁，另外一个线程获得锁，进入又想实例化，会判断是否进行实例化了，如果存在，就不进行实例化了。

#### 静态内部类

```java
//一个延迟实例化的内部类的单例模式
public final class Singleton {
 
    //一个内部类的容器，调用getInstance时，JVM加载这个类
    private static final class SingletonHolder {
        static final Singleton singleton =  new Singleton();
    }
 
    private Singleton() {}
 
    public static Singleton getInstance() {
        return SingletonHolder.singleton;
    }
 }
 ```

首先，其他类在引用这个Singleton的类时，只是新建了一个引用，并没有开辟一个的堆空间存放（对象所在的内存空间）。接着，当使用Singleton.getInstance()方法后，Java虚拟机（JVM）会加载SingletonHolder.class（JLS规定每个class对象只能被初始化一次），并实例化一个Singleton对象。

缺点：需要在Java的另外一个内存空间（Java PermGen 永久代内存，这块内存是虚拟机加载class文件存放的位置）占用一个大块的空间。

参考：[wikipedia.org](http://en.wikipedia.org/wiki/Initialization-on-demand_holder_idiom)

#### 枚举

```java
public enum Singleton {  
    INSTANCE;  
    public void whateverMethod() {  
    }  
}  
```

这种方式是Effective Java作者Josh Bloch 提倡的方式，它不仅能避免多线程同步问题，而且还能防止反序列化重新创建新的对象。

通过这种方式，不能通过反射和序列化来获取一个实例，因为所有的枚举类都继承自java.lang.Enum类, 而不是Object类。见Enum源码：

```java
protected final Object clone() throws CloneNotSupportedException {  
    throw new CloneNotSupportedException();  
} 

private void readObject(ObjectInputStream in) throws IOException,  
        ClassNotFoundException {  
            throw new InvalidObjectException("can't deserialize enum");  
}  
  
private void readObjectNoData() throws ObjectStreamException {  
        throw new InvalidObjectException("can't deserialize enum");  
}
```

摘自：[javachen.com](http://blog.javachen.com/2013/06/09/note-about-java-singleton-model.html)
