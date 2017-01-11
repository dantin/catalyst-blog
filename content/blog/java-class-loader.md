+++
date = "2016-12-12T23:11:10+08:00"
title = "Java中的ClassLoader"
categories = ["Engineering"]
tags = ["Java"]
description = "本文记录Java的类加载机制"
slug = "java-class-loader"
+++

### 什么是ClassLoader?

当我们写好一个Java程序之后，不是管是CS还是BS应用，都是由若干个.class文件组织而成的一个完整的Java应用程序。当程序在运行时，即会调用该程序的一个入口函数来调用系统的相关功能，而这些功能都被封装在不同的class文件当中，所以经常要从这个class文件中要调用另外一个class文件中的方法，如果另外一个文件不存在的，则会引发系统异常。而程序在启动的时候，并不会一次性加载程序所要用的所有class文件，而是根据程序的需要，通过Java的类加载机制（ClassLoader）来动态加载某个class文件到内存当中的，从而只有class文件被载入到了内存之后，才能被其它class所引用。所以ClassLoader就是用来动态加载class文件到内存当中用的。

### Java默认提供的三个ClassLoader

#### BootStrap ClassLoader

BootStrap ClassLoader：称为启动类加载器，是Java类加载层次中最顶层的类加载器，负责加载JDK中的核心类库，如：rt.jar、resources.jar、charsets.jar等，可通过如下程序获得该类加载器从哪些地方加载了相关的jar或class文件：

```java
URL[] urls = sun.misc.Launcher.getBootstrapClassPath().getURLs();  
for (int i = 0; i < urls.length; i++) {  
    System.out.println(urls[i].toExternalForm());  
}
```

在本机JDK环境获得的结果：

```console
file:/Library/Java/JavaVirtualMachines/jdk1.8.0_60.jdk/Contents/Home/jre/lib/resources.jar
file:/Library/Java/JavaVirtualMachines/jdk1.8.0_60.jdk/Contents/Home/jre/lib/rt.jar
file:/Library/Java/JavaVirtualMachines/jdk1.8.0_60.jdk/Contents/Home/jre/lib/sunrsasign.jar
file:/Library/Java/JavaVirtualMachines/jdk1.8.0_60.jdk/Contents/Home/jre/lib/jsse.jar
file:/Library/Java/JavaVirtualMachines/jdk1.8.0_60.jdk/Contents/Home/jre/lib/jce.jar
file:/Library/Java/JavaVirtualMachines/jdk1.8.0_60.jdk/Contents/Home/jre/lib/charsets.jar
file:/Library/Java/JavaVirtualMachines/jdk1.8.0_60.jdk/Contents/Home/jre/lib/jfr.jar
file:/Library/Java/JavaVirtualMachines/jdk1.8.0_60.jdk/Contents/Home/jre/classes
```

#### Extension ClassLoader

Extension ClassLoader：称为扩展类加载器，负责加载Java的扩展类库，默认加载JAVA_HOME/jre/lib/ext/目下的所有jar。

#### App ClassLoader

App ClassLoader：称为系统类加载器，负责加载应用程序classpath目录下的所有jar和class文件。

_注意_： 除了Java默认提供的三个ClassLoader之外，用户还可以根据需要定义自已的ClassLoader，而这些自定义的ClassLoader都必须继承自java.lang.ClassLoader类，也包括Java提供的另外二个ClassLoader（Extension ClassLoader和App ClassLoader）在内，但是Bootstrap ClassLoader不继承自ClassLoader，因为它不是一个普通的Java类，底层由C++编写，已嵌入到了JVM内核当中，当JVM启动后，Bootstrap ClassLoader也随着启动，负责加载完核心类库后，并构造Extension ClassLoader和App ClassLoader类加载器。

### ClassLoader加载类的原理

#### 原理介绍

ClassLoader使用的是__双亲委托模型__来搜索类的，每个ClassLoader实例都有一个父类加载器的引用（不是继承的关系，是一个包含的关系），虚拟机内置的类加载器（Bootstrap ClassLoader）本身没有父类加载器，但可以用作其他ClassLoader实例的父类加载器。

当一个ClassLoader实例需要加载某个类时，它会试图亲自搜索某个类之前，先把这个任务委托给它的父类加载器，这个过程是由上至下依次检查的，首先由最顶层的类加载器Bootstrap ClassLoader试图加载，如果没加载到，则把任务转交给Extension ClassLoader试图加载，如果也没有加载到，则转交给App ClassLoader进行加载，如果它也没有加载得到的话，则返回给委托的发起者，由它到指定的文件系统或网络等URL中加载该类。

如果它们都没有加载到这个类时，则抛出ClassNotFoundException异常。否则，将这个找到的类生成一个类的定义，并将它加载到内存当中，最后返回这个类在内存中的Class实例对象。

#### 为什么要使用双亲委托这种模型呢？

因为这样可以__避免重复加载__。当父类已经加载了该类的时候，就没有必要子ClassLoader再加载一次。

考虑到安全因素，我们试想一下，如果不使用这种委托模式，那我们就可以随时使用自定义的String来动态替代java核心api中定义的类型，这样会存在非常大的安全隐患，而双亲委托的方式，就可以避免这种情况，因为String已经在启动时就被引导类加载器（Bootstrcp ClassLoader）加载，所以用户自定义的ClassLoader永远也无法加载一个自己写的String，除非你改变JDK中ClassLoader搜索类的默认算法。

#### JVM在搜索类的时候，又是如何判定两个class是相同的呢？

JVM在判定两个class是否相同时，不仅要判断两个类名是否相同，而且要判断是否由同一个类加载器实例加载的。只有两者同时满足的情况下，JVM才认为这两个class是相同的。

就算两个class是同一份class字节码，如果被两个不同的ClassLoader实例所加载，JVM也会认为它们是两个不同class。

比如网络上的一个Java类org.classloader.simple.NetClassLoaderSimple，javac编译之后生成字节码文件NetClassLoaderSimple.class，ClassLoaderA和ClassLoaderB这两个类加载器并读取了NetClassLoaderSimple.class文件，并分别定义出了java.lang.Class实例来表示这个类，对于JVM来说，它们是两个不同的实例对象，但它们确实是同一份字节码文件，如果试图将这个Class实例生成具体的对象进行转换时，就会抛运行时异常java.lang.ClassCaseException，提示这是两个不同的类型。

### ClassLoader的体系架构

```console
 +-----------------------------+
 |                             |
 |  ClassLoader Architecture   |
 |                             |
 |  +-----------------------+  |    +------------------------------+
 |  |                       |  |    |                              |
 |  | Bootstrap ClassLoader |--+--->| Load JRE\lib\rt.jar 或       |
 |  |                       |  |    | -Xbootclasspath指定的Jar包    |
 |  +-----------------------+  |    |                              |
 |             |               |    +------------------------------+
 |             |               |
 |             |               |
 |  +-----------------------+  |    +------------------------------+
 |  |                       |  |    |                              |
 |  | Extension ClassLoader |--+--->| Load JRE\lib\ext\*.jar  Or   |
 |  |                       |  |    | -Djava.ext.dirs指定目录下的JAR |
 |  +-----------------------+  |    |                              |
 |             |               |    +------------------------------+
 |             |               |
 |             |               |
 |  +-----------------------+  |    +------------------------------+
 |  |                       |  |    |                              |
 |  |     App ClassLoader   |--+--->| Load CLASSPATH或-Djava.class |
 |  |                       |  |    | .path指定的目录下的类和JAR包    |
 |  +-----------------------+  |    |                              |
 |             |               |    +------------------------------+
 |             |               |
 |             |               |
 |  +-----------------------+  |    +------------------------------+
 |  |                       |  |    |                              |
 |  |   Custom ClassLoader  |--+--->| 通过java.lang.ClassLoader的子 |
 |  |                       |  |    | 类自定义加载的Class            |
 |  +-----------------------+  |    |                              |
 |                             |    +------------------------------+
 +-----------------------------+

```

#### 验证ClassLoader加载类的原理

测试1：打印ClassLoader类的层次结构，请看下面这段代码：

```java
ClassLoader loader = ClassLoaderTest.class.getClassLoader();    //获得加载ClassLoaderTest.class这个类的类加载器  
while(loader != null) {  
    System.out.println(loader);  
    loader = loader.getParent();    //获得父类加载器的引用  
}  
System.out.println(loader);
```

打印结果为：

```console
sun.misc.Launcher$AppClassLoader@5fa6fb3e
sun.misc.Launcher$ExtClassLoader@4bb8d481
null
```

第一行结果说明：ClassLoaderTest的类加载器是AppClassLoader。

第二行结果说明：AppClassLoader的类加器是ExtClassLoader，即parent=ExtClassLoader。

第三行结果说明：ExtClassLoader的类加器是Bootstrap ClassLoader，因为Bootstrap ClassLoader不是一个普通的Java类，所以ExtClassLoader的parent=null，所以第三行的打印结果为null就是这个原因。

测试2：将ClassLoaderTest.class打包成ClassLoaderTest.jar，放到Extension ClassLoader的加载目录下（JAVA_HOME/jre/lib/ext），然后重新运行这个程序，得到的结果会是什么样呢？

```console
sun.misc.Launcher$ExtClassLoader@4bb8d481
null
```

为什么第一行的结果是ExtClassLoader呢？

因为ClassLoader的委托模型机制，当我们要用ClassLoaderTest.class这个类的时候，AppClassLoader在试图加载之前，先委托给Bootstrcp ClassLoader，Bootstracp ClassLoader发现自己没找到，它就告诉ExtClassLoader，兄弟，我这里没有这个类，你去加载看看，然后Extension ClassLoader拿着这个类去它指定的类路径（JAVA_HOME/jre/lib/ext）试图加载，唉，它发现在ClassLoaderTest.jar这样一个文件中包含ClassLoaderTest.class这样的一个文件，然后它把找到的这个类加载到内存当中，并生成这个类的Class实例对象，最后把这个实例返回。所以ClassLoaderTest.class的类加载器是ExtClassLoader。

第二行的结果为null，是因为ExtClassLoader的父类加载器是Bootstrap ClassLoader。

参考：
[csdn](http://blog.csdn.net/xyang81/article/details/7292380)