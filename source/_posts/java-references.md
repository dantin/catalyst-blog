title: Java的引用类型
date: 2016-06-04 22:43:59
categories: 工程
tags: Java
toc: true
---

引用类型是Java语言的一个核心概念。对于一个对象来说，只要有引用的存在，它就会一直存在于内存中。如果这样的对象越来越多，超出了JVM中的内存总数，JVM就会抛出OutOfMemory错误。虽然垃圾回收的具体运行是由JVM来控制的，但是开发人员仍然可以在一定程度上与垃圾回收器进行交互，其目的在于更好的帮助垃圾回收器管理好应用的内存。这种交互方式就是使用JDK 1.2引入的java.lang.ref包。

### 强引用

在一般的Java程序中，见到最多的就是强引用（Strong Reference）。如`Date date = new Date()`，date就是一个对象的强引用。对象的强引用可以在程序中到处传递。很多情况下，会同时有多个引用指向同一个对象。强引用的存在限制了对象在内存中的存活时间。假如对象A中包含了一个对象B的强引用，那么一般情况下，对象B的存活时间就不会短于对象A。如果对象A没有显式的把对象B的引用设为null的话，就只有当对象A被垃圾回收之后，对象B才不再有引用指向它，才可能获得被垃圾回收的机会。

除了强引用之外，java.lang.ref包中提供了对一个对象的不同的引用方式。JVM的垃圾回收器对于不同类型的引用有不同的处理方式。

### 软引用

软引用（Soft Reference）在强度上弱于强引用，通过类`SoftReference`来表示。它的作用是告诉垃圾回收器，程序中的哪些对象是不那么重要，当内存不足的时候是可以被暂时回收的。当JVM中的内存不足的时候，垃圾回收器会释放那些只被软引用所指向的对象。如果全部释放完这些对象之后，内存还不足，才会抛出OutOfMemory错误。软引用非常适合于创建缓存。当系统内存不足的时候，缓存中的内容是可以被释放的。

比如：考虑一个图像编辑器的程序。该程序会把图像文件的全部内容都读取到内存中，以方便进行处理。而用户也可以同时打开多个文件。当同时打开的文件过多的时候，就可能造成内存不足。如果使用软引用来指向图像文件内容的话，垃圾回收器就可以在必要的时候回收掉这些内存。

```java
public class ImageData {
    private String path;
    private SoftReference<byte[]> dataRef;
    public ImageData(String path) {
        this.path = path;
        dataRef = new SoftReference<byte[]>(new byte[0]);
    }
    private byte[] readImage() {
        //省略了读取文件的操作
        return new byte[1024 * 1024];
  }
    public byte[] getData() {
        byte[] dataArray = dataRef.get();
        if (dataArray == null || dataArray.length == 0) {
            dataArray = readImage();
            dataRef = new SoftReference<byte[]>(dataArray);
        }
        return dataArray;
    }
}
```
在运行上面程序的时候，可以使用`-Xmx`参数来限制JVM可用的内存。由于软引用所指向的对象可能被回收掉，在通过get方法来获取软引用所实际指向的对象的时候，总是要检查该对象是否还存活。

### 弱引用

弱引用（Weak Reference）在强度上弱于软引用，通过类`WeakReference`来表示。它的作用是引用一个对象，但是并不阻止该对象被回收。如果使用一个强引用的话，只要该引用存在，那么被引用的对象是不能被回收的。弱引用则没有这个问题。在垃圾回收器运行的时候，如果一个对象的所有引用都是弱引用的话，该对象会被回收。弱引用的作用在于解决强引用所带来的对象之间在存活时间上的耦合关系。弱引用最常见的用处是在集合类中，尤其在哈希表中。哈希表的接口允许使用任何Java对象作为键来使用。当一个键值对被放入到哈希表中之后，哈希表对象本身就有了对这些键和值对象的引用。如果这种引用是强引用的话，那么只要哈希表对象本身还存活，其中所包含的键和值对象是不会被回收的。如果某个存活时间很长的哈希表中包含的键值对很多，最终就有可能消耗掉JVM中全部的内存。

对于这种情况的解决办法就是使用弱引用来引用这些对象，这样哈希表中的键和值对象都能被垃圾回收。Java中提供了`WeakHashMap`来满足这一常见需求。

### 幽灵引用

在介绍幽灵引用之前，要先介绍Java提供的_对象终止化机制_（finalization）。在Object类里面有个`finalize`方法，其设计的初衷是在一个对象被真正回收之前，可以用来执行一些清理的工作。因为Java并没有提供类似C++的析构函数一样的机制，就通过 finalize方法来实现。但是问题在于垃圾回收器的运行时间是不固定的，所以这些清理工作的实际运行时间也是不能预知的。幽灵引用（phantom reference）可以解决这个问题。在创建幽灵引用PhantomReference的时候必须要指定一个引用队列。当一个对象的finalize方法已经被调用了之后，这个对象的幽灵引用会被加入到队列中。通过检查该队列里面的内容就知道一个对象是不是已经准备要被回收了。

幽灵引用及其队列的使用情况并不多见，主要用来实现比较精细的内存使用控制，这对于移动设备来说是很有意义的。程序可以在确定一个对象要被回收之后，再申请内存创建新的对象。通过这种方式可以使得程序所消耗的内存维持在一个相对较低的数量。比如下面的代码给出了一个缓冲区的实现示例。

```java
public class PhantomBuffer {
    private byte[] data = new byte[0];
    private ReferenceQueue<byte[]> queue = new ReferenceQueue<byte[]>();
    private PhantomReference<byte[]> ref = new PhantomReference<byte[]>(data, queue);
    public byte[] get(int size) {
        if (size <= 0) {
            throw new IllegalArgumentException("Wrong buffer size");
        }
        if (data.length < size) {
            data = null;
            System.gc(); //强制运行垃圾回收器
             try {
                queue.remove(); //该方法会阻塞直到队列非空
                ref.clear(); //幽灵引用不会自动清空，要手动运行
                ref = null;
                data = new byte[size];
                ref = new PhantomReference<byte[]>(data, queue);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
       }
       return data;
    }
}
```

在上面的代码中，每次申请新的缓冲区的时候，都首先确保之前的缓冲区的字节数组已经被成功回收。引用队列的remove方法会阻塞直到新的幽灵引用被加入到队列中。不过需要注意的是，这种做法会导致垃圾回收器被运行的次数过多，可能会造成程序的吞吐量过低。

### 引用队列

在有些情况下，程序会需要在一个对象的可达到性发生变化的时候得到通知。比如某个对象的强引用都已经不存在了，只剩下软引用或是弱引用。但是还需要对引用本身做一些的处理。典型的情景是在哈希表中。引用对象是作为WeakHashMap中的键对象的，当其引用的实际对象被垃圾回收之后，就需要把该键值对从哈希表中删除。有了引用队列（ReferenceQueue），就可以方便的获取到这些弱引用对象，将它们从表中删除。在软引用和弱引用对象被添加到队列之前，其对实际对象的引用会被自动清空。通过引用队列的poll/remove方法就可以分别以非阻塞和阻塞的方式获取队列中的引用对象。
