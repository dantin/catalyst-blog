+++
date = "2016-06-02T22:24:30+08:00"
title = "深入理解Java虚拟机之二：对象的创建、内存布局及访问方式"
categories = ["Scholar"]
tags = ["Java", "JVM"]
description = "本文记录Java虚拟机中，对象的创建、内存布局及其访问方式"
slug = "java-jvm-object"
+++

### 对象的创建

语言层面上，对象的创建不过是一个`new`关键字而已，那么在虚拟机中的过程又是怎样的呢？

1. 判断类是否加载。

    虚拟机遇到一条`new`指令的时候，它首先会检查这个指令的参数是否能在常量池中定位到一个类的符号引用，并且检查这个符号代表的类是否被加载、解析并初始化。如果没有完成这个过程，则必须执行相应类的加载。

2. 在堆上为对象分配空间。

    对象需要的空间大小在类加载完成后便能确定。之后便是在堆上为该对象分配固定大小的空间。

    分配的方式有两种：

    * 如果使用Serial、ParNew等带Compact过程的收集器，Java内存中的堆都是规整的，只需把作为使用和未使用空间的分界点的指针移动一段距离就可以了。

    * 如果使用CMS这种基于Mark-Sweep算法的收集器，Java内存并不是规整的，虚拟机就要维护了一个列表来记录内存的使用情况，这种方式叫做“空闲列表”的方式。

    虚拟机为对象分配空间是非常频繁的，如果同时为多个线程分配对象，就涉及到并发安全控制了。一般也有两个解决方案：

    1. 对分配内存空间的动作进行同步，即：使用CAS配上失败重试的方式保证更新操作的原子性。
    2. 把内存分配的动作分配在不同的空间中进行，即：每个线程在Java堆中预先分配一小块内存，称之为本地线程分配缓冲（Thread Local Allocation Buffer,TLAB）。哪个线程要分配内存，就在哪个线程的TLAB上分配。只有TLAB使用完并需要分配新的TLAB的时候才需要同步锁定。

3. 初始化内存空间。

    内存分配完成之后，虚拟机会将分配空间内都初始化为零值（不包括对象头），如果使用TLAB分配，这一过程也可以提前至TLAB分配时进行。

4. 设置对象的对象头。

    接下来虚拟机要设置对象的对象头。包括对象的哈希码、类元素信息、GC分代年龄等。这些信息都放置在对象头中。

5. 执行<init>方法，初始化对象内成员。

执行完这五步，一个对象才算是真正产生。

### 对象的内存布局

内存中，对象存储布局可分为三部分：对象头(Header)，示例数据(Instance Data)和对齐填充(Padding)。

1. 对象头：包括两部分信息。

    第一部分用于存储对象自身的运行时数据，如哈希码，GC分代年龄、锁状态、线程持有锁、等等。这部分数据的长度在32为或64位，官方称之为“Mark Word”。

    对象头的另一部分是类型指针，即对象指向它的类元素的指针，通过这个指针来确定这个对象时那个类的实例。（如果Java对象是一个数组，则对象头还必须有一块用于记录数组长度的数据。因为Java数组元数据中没有数组大小的记录）

2. 实例数据：这部分是真正用来存储对象有效信息的地方。

3. 对齐填充：这部分并不是必需存在的，只是起着占位符的作用。因为HotSpot虚拟机要求对象起始地址必须是8字节的倍数。

### 对象的访问方式

我们可以通过使用栈上的reference数据来操作堆上的具体对象。

有两种方式来访问具体对象：句柄和直接指针。

* 句柄：Java堆中划分出一个句柄池，专门用来存放对象的实例地址和类型地址。而栈中的reference只是该句柄池中某一句柄的地址。好处是当进行垃圾回收并被移动后，对象地址改变而reference的数据不用改变。

* 直接指针：reference直接指向某一对象的地址。好处便是速度快，节省了一次定位的时间开销。
