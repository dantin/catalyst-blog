---
title: Java类的生命周期
date: 2016-09-08 17:40:00
categories: 工程
tags: Java
toc: true
---

和Java对象一样，Java类也有生命周期，本文主要介绍Java类的生命周期。

### 加载

类加载指的是类的生命周期中加载、连接、初始化三个阶段。

在加载阶段，虚拟机需要完成以下3件事：

1. 通过一个类的全限定名来获取定义此类的二进制字节流。
2. 将这个字节流代表的静态存储结构转化为为方法区的运行时数据结构。
3. 在内存中生成一个代表这个类的`java.lang.Class`对象，作为方法区这个类各种数据的访问入口。

![Java类的生命周期](/images/java-class-lifecycle.jpg "Java class lifecycle")

### 连接

连接阶段比较复杂，一般会跟加载阶段和初始化阶段交叉进行，这个阶段的主要任务就是做一些加载后的验证工作以及一些初始化前的准备工作，可以细分为三个步骤：验证、准备和解析。

#### 验证

当一个类被加载之后，必须要验证一下这个类是否合法，比如这个类是不是符合字节码的格式、变量与方法是不是有重复、数据类型是不是有效、继承与实现是否合乎标准等等。总之，这个阶段的目的就是保证加载的类是能够被jvm所运行，并且不会危害虚拟机自身的安全，例如说数组越界访问。

#### 准备

准备阶段的工作就是为类的静态变量分配内存并设为jvm默认的初值，对于非静态的变量，则不会为它们分配内存，这些变量使用的内存都将在方法区中分配。有一点需要注意，这时候，静态变量的初值为jvm默认的初值，而不是我们在程序中设定的初值。jvm默认的初值是这样的：

1. 基本类型（int、long、short、char、byte、boolean、float、double）的默认值为0。
2. 引用类型的默认值为null。
3. 常量的默认值为我们程序中设定的值，比如我们在程序中定义final static int a = 100，则准备阶段中a的初值就是100。

#### 解析

这一阶段的任务就是把常量池中的符号引用转换为直接引用。

* 符号引用：符号引用以一组符号来描述所引用的目标，符号引用可以是任何形式的字面量，只有使用时能无歧义地定位到目标即可。此时目标不一定在内存中。
* 直接引用：直接引用可以是直接指向目标的指针，相对偏移量或者一个能间接定位到目标的句柄。此时目标已经在内存中。

连接阶段完成之后会根据使用的情况（主动引用还是被动引用）来选择是否对类进行初始化。

### 初始化

类初始化阶段是类加载过程的最后一步，前面的类加载过程中，除了加载阶段用户应用程序可以通过自定义的类加载器参与之外，其余动作由虚拟机主导和控制。到了本阶段，才真正开始执行类中定义的代码。

初始化过程是执行类构造器`<clinit>()`方法的过程。`<clinit>()`方法是由编译器自动收集类中所有类变量赋值操作和静态语句块中的语句合并产生的，编译器收集的顺序是由语句在源文件中出现的顺序决定的。

静态语句块中只能访问到定义在静态语句块之前的变量，定义在它之后的变量，在前面的静态语句块可以赋值，但不能访问。

1. 虚拟机保证父类的`<clinit>()`方法在子类的`<clinit>()`之前被执行。
2. 虚拟机保证`<clinit>()`在多线程环境中被正确地加锁，同步，同一个类加载器下，一个类`<clinit>()`方法只会被执行一次。

### 使用

#### 主动引用

如果一个类被主动引用，就会触发类的初始化。在java中，主动引用的情况有：

1. 通过new关键字实例化对象、读取或设置类的静态变量、调用类的静态方法。
2. 通过反射方式执行以上三种行为。
3. 初始化子类的时候，会触发父类的初始化。
4. 作为程序入口直接运行时（也就是直接调用main方法）。

#### 被动引用

1. 引用父类的静态字段，只会引起父类的初始化，而不会引起子类的初始化。
2. 定义类数组，不会引起类的初始化。
3. 引用类的常量，不会引起类的初始化。

当使用阶段完成之后，java类就进入了卸载阶段。

### 卸载

在类使用完之后，如果满足下面的情况，类就会被卸载：

1. 该类所有的实例都已经被回收，也就是java堆中不存在该类的任何实例。
2. 加载该类的ClassLoader已经被回收。
3. 该类对应的java.lang.Class对象没有任何地方被引用，没有在任何地方通过反射访问该类的方法。

如果以上三个条件全部满足，jvm就会在方法区垃圾回收的时候对类进行卸载，类的卸载过程其实就是在方法区中清空类信息，java类的整个生命周期就结束了。

由Java虚拟机自带的类加载器所加载的类，在虚拟机的生命周期中，始终不会被卸载。Java虚拟机自带的类加载器包括根类加载器、扩展类加载器和系统类加载器。Java虚拟机本身会始终引用这些类加载器，而这些类加载器则会始终引用它们所加载的类的Class对象，因此这些Class对象始终是可触及的。

由用户自定义的类加载器加载的类是可以被卸载的。

![Java类的内存使用](/images/java-class-memory.png "Java class memory usage")

### 类加载器

* 启动类加载器（Bootstrap ClassLoader）：加载lib/中类，不可直接使用
* 扩展类加载器（Extension ClassLoader）：加载lib/ext/的类库，可直接使用
* 应用程序类加载器（Application ClassLoader）：负责加载用户类路径上所指定的类，可直接使用。

#### 双亲委派模型

如果一个类加载器收到了类加载的请求，他不会自己去尝试加载这个类，而是把请求委派给父类加载器去完成。只有父加载器反馈自己无法完成加载请求时，子加载器才会尝试自己去加载。

参考
[xiaohansong的wiki](http://wiki.xiaohansong.com/java/class_lifecycle.html)