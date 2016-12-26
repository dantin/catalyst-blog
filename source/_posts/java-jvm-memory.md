---
title: 深入理解Java虚拟机之一：虚拟机内存划分
date: 2016-06-01 23:29:36
categories: 学术
tags: [Java, JVM]
toc: true
---

Java虚拟机在运行时把内存区域大致分为七部分，分别是：程序计数器、Java虚拟机栈、本地方法栈、方法区、Java堆、运行时常量池、直接内存。它们拥有各自的特性和作用，有些随着进程的启动而创建，随着进程结束而销毁，而另一些则始终贯穿于虚拟机的整个生命周期。

![JVM架构图](/images/jvm_architecture.png "JVM architecture")

JVM架构图中，蓝色区域包裹的部分是运行时的几个数据区域，其中：
* 白色的部分为线程私有的，它随着线程的启动而创建。每个线程都拥有各自的内存区域，分别为：JAVA栈（Java Stack）、本地方法栈(Native Method Stack)和程序计数器（Program Counter Register）。
* 黄色部分是线程共享的，所有的线程共享该区域的内容。它们是：方法区（Method Area），堆（Heap）。

### 线程私有区域

首先介绍线程私有区域。

#### 程序计数器

__Program Counter Register__

学过计算机组成原理的都知道计算机处理器中的程序计数器。当处理器执行一条指令时，首先需要根据PC中存放的指令地址，将指令由内存取到指令寄存器中，此过程称为“取指令”。与此同时，PC中的地址或自动加1或由转移指针给出下一条指令的地址。此后经过分析指令，执行指令。完成第一条指令的执行，而后根据PC取出第二条指令的地址，如此循环，执行每一条指令。

处理器的程序计数器是指寄存器，而Java程序计数器是指一小块内存空间。

Java代码编译字节码之后，虚拟机会一行一行的解释字节码，并翻译成本地代码。这个程序计数器中存放的，就是当前线程所执行的字节码行号的指示器。在虚拟机概念模型中，字节码解释器工作就是通过改变这个计数器的值来选取下一条需要执行的字节码指令，分支、循环、跳转、异常处理等都依赖于它。

Java虚拟机的多线程是通过线程轮流切换并分配处理器执行时间的方式实现的，因此为了线程切换后还能恢复执行位置，每个线程都需要拥有一个独立的程序计数器。

如果线程正在执行的是一个Java方法，这个计数器记录的是正在执行的虚拟机字节码指令的地址；如果执行的是Java Native方法，这个计数器值为空。

程序计数器是Java虚拟机中没有规定任何OutOfMemoryError的区域。
 
#### 虚拟机栈

__Java Stack__又称为_VM Stack_

虚拟机栈（VM Stack）也是线程私有的，它的生命周期也和线程相同。它存放的是Java方法执行时的数据：
* 每个方法开始执行的时候，都会创建一个栈帧（Stack Frame）用于储存局部变量表、栈操作数、动态链接、方法出口等信息。
* 每个方法从调用到执行完成就对应一个栈帧在虚拟机栈中入栈到出栈的过程。

经常有人把Java内存分为堆内存和栈内存，这种是比较粗糙的分法，很大原因是，大多数程序员最关注的、与对象内存分配最密切的区域就是堆和栈。

局部变量表存放的是编译器可知的各种基本数据类型(boolean 、byte、int、long、char、short、float、double)、对象引用（reference类型）和returnAddress类型（它指向了一条字节码指令的地址）。

其中64bit长度的long和double会占用两个局部变量空间(Slot)，其余的数据类型只占用一个。

局部变量表所需的内存空间是在编译时期确定的，在方法运行期间不会改变局部变量表的大小。

在Java虚拟机规范中，对这部分区域规定了两种异常：

1. 当一个线程的栈深度大于虚拟机所允许的深度的时候，将会抛出StackOverflowError异常；
2. 如果当创建一个新的线程时无法申请到足够的内存，则会抛出OutOfMemeryError异常。

#### 本地方法栈

__Native Method Stack__

本地方法栈（Native Method Stack）与虚拟机栈所发挥的作用是十分相似的，他们之间的区别不过是虚拟机栈为Java方法字节码服务，而本地方法栈则为Native方法服务。

在虚拟机规范中对本地方法使用的语言和使用方法与数据结构没有强制规定，因此具体的虚拟机可以自由实现它。Sun HotSpot虚拟机把本地方法栈和虚拟机栈合二为一。

和虚拟机栈一样，本地方法栈也会抛出OutOfMemoryError 和 StackOverflowError异常。

### 线程共享区域

接下来我们介绍的都是所有线程共享的区域了。

#### 堆

__Heap__

堆（Heap）是虚拟机中最大的一块内存区域了，被所有线程共享，在虚拟机启动时创建。它的目的便是存放对象实例。

堆是垃圾收集器管理的主要区域，因此，很多时候也被成为‘GC’堆（Garbage Collected Heap）。

![JVM内存结构](/images/jvm_memory_structure.png "JVM memery structure")

* 从垃圾回收的角度来讲，现在的收集器包括HotSpot都采用分代收集算法，所以堆又可以分为：新生代（Young）和老年代（Tenured），再细致一点，新生代又可分为Eden、From Survivor空间和To Survivor空间。
* 从内存分配的角度来讲，又可以分为若干个线程私有的分配缓冲区（Thread Local Allocation Buffer ,TLAB）。

当堆空间不足切无法扩展，会抛出OutOfMemoryError异常。
 
#### 方法区

__Method Area__

方法区（Method Area）与Java堆一样，是各个线程共享的内存区域，用于存储被虚拟机加载的类信息、常量、静态变量、即时编译器编译后的代码等数据。
它有个别名叫做非堆Non-Heap。

对于HotSpot开发者来说，很多人称它为“永久代”（Permanent Generation），但是两者并不等价，仅仅是因为HotSpot虚拟机设计团队把GC分代收集扩展至方法区，或者说使用永久代来实现方法区而已，这样HotSpot的垃圾收集器可以向管理堆一样管理这部分内存。但是因为永久代有`-XX：MaxPermSize`的上限，使其更容易内存溢出。因此在JDK1.7的HotSpot中，已经把原本放在永久代的字符串常量池移出去了。

![方法区内存结构](/images/jvm-method-area.jpg "JVM method area")

当方法区无法满足内存分配需求的时候，会抛出OutOfMemoryError异常。

#### 常量池

__Runtime Constant Pool__

运行时常量池（Runtime Constant Pool）是方法区的一部分。

Class文件中除了类的版本、字段、方法、接口等信息外，还有一项信息是常量池（Constant Pool Table），用于存放编译器生成的各种字面量和符号引用，这些内容将在类加载后进入方法区存放。

运行时常量池相对于Class文件常量池的另外一个重要特征是具有动态性，运行期间也可能有新的常量放入池中，比如：String.intern()方法。

运行时常量池属于方法区一部分，自然会抛出OutOfMemoryError异常。

#### 直接内存

__Direct Memory__

直接内存（Direct Memory）不属于虚拟机中定义的内存区域，而是堆外内存。

JDK1.4 中新加入了NIO(new Input/Output)类，引入了一种基于通道（Channel）和缓冲区（Buffer）的I/O方式，它可以使用Native函数直接分配堆外内存，然后通过Java堆中的DirectByteBuffer对象作为这快内存的引用进行操作。这样能在一些场景中显著提高新能性能。

如果直接内存不足时，会抛出OutOfMemoryError异常。
