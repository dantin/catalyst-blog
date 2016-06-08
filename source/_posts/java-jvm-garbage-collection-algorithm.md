title: 深入理解java虚拟机之四：垃圾收集算法及HotSpot实现
date: 2016-06-07 09:57:08
categories: 学术
tags: [Java, JVM]
toc: true
---

一般来说，垃圾收集算法分为四类：

### 标记-清除算法

最基础的算法是标记-清除算法（Mark-Sweep）。回收过程包括“标记”和“清除”两个阶段

* 标记阶段时，标识出可回收的引用。
* 清除阶段时，对标记阶段所标识为的对像进行回收。

![标记-清除算法](/images/jvm_mark_sweep.gif "Mark-Sweep")

这是最简单的一种算法，但是缺点也是很明显的：一个是效率问题，标记和清除效率都不高。二是空间问题，清除之后会产生大量的空间碎片，导致之后分配大对象找不到足够的连续对象而不得不触发另一次垃圾收集动作。

### 复制算法

复制算法（Copying）将可用内存按照容量大小分成相等的两份，每次只使用一半。当这一块内存用完了，就会将还存活的对象复制到另一块内存上，然后将之前的那块内存清空。优点是解决了空间碎片的问题，而且分配新对象的时候顺序分配，实现简单，运行高效。缺点是内存减小了一半。算法示意图如下:

![复制算法](/images/jvm_gc_copying.gif "Copying")

现在的商业虚拟机都采用这种收集算法来回收新生代。由于新生代对象死亡率较高，所以可以将内存分为一块较大的Eden空间和两块较小的Survivor空间，每次使用Eden和一块Survivor。当回收时，将Eden和一块Survivor中还存活的对象复制到另一块Survivor上，然后清理掉Eden和之前使用的Survivor空间。

HotSpot虚拟机默认Eden和Survivor比例为8:1，也就是只有10%的内存会被“浪费”。

Young区和Old区使用的回收对象算法不一样，因为回收Young区满了需要回收时，Old不需要被回收，而当Old区满了要回收对象时，整个内存堆都要清理，而且使用者可以设置Young区和old区的回收是多线程还是单线程的，所以设计者是希望对象能够多点时间留在Young区，以提高回收对象的效率。设计成From和To两个平行的区，我觉得是为了筛选真正符合Old区的要求的对象（即需要长时间持有的引用的对象），然后再将他们放入Old区。 

### 标记-整理算法

复制算法在对象存活率较高的情况下，效率会变低。而且浪费了50%的空间。

根据老年代的特点，有人提出了另外一种“标记-整理”算法（Mark-Compact）。算法的也分为标记和整理两个阶段。标记和“标记-清除”算法的标记过程一样。当标记完成之后，并不直接对可回收对象进行整理，而是所有存活的对象整理成连续的，然后清理掉剩余的空间。算法示意图如下。

![标记-整理算法](/images/jvm_mark_compact.gif "Mark-Compact")

### 分代收集算法

当前商业虚拟机都采用“分代收集”（Generational Collection）算法，根据对象存活的周期不同将内存划分为几块。一般是将Java堆分为新生代和老年代，这样就可以根据各个年代的特点采用最适当的收集算法。新生代采用复制算法，年老带采用标记-清理或者标记-整理算法。

![分代收集算法](/images/jvm_hotspot_model.jpg "Generational Collection")

#### 年轻代(Young Gen)  

年轻代特点是_区域相对tenure较小_默认推荐与tenure比例是3:8，但需要系统特点可调整），_对像存活率低_。

这种情况复制算法的回收整理，速度是最快的。_复制算法的效率只和当前存活对像大小有关_，因而很适用于年轻代的回收。而复制算法内存利用率不高的问题，通过HotSpot中的两个survivor的设计得到缓解。

#### 老年代(Tenure Gen)

老年代的特点是区域较大，对像存活率高。

这种情况，存在大量存活率高的对像，复制算法明显变得不合适。一般是由标记清除或者是标记清除与标记整理的混合实现。

_Mark阶段的开销与存活对像的数量成正比_，这点上说来，对于老年代，标记清除或者标记整理有一些不符，但可以通过多核/线程利用，对并发、并行的形式提标记效率。

_Sweep阶段的开销与所管理区域的大小成正相关_，但Sweep“就地处决”的特点，回收的过程没有对像的移动。使其相对其它有对像移动步骤的回收算法，仍然是效率最好的。但是需要解决内存碎片问题。

_Compact阶段的开销与存活对像的数据成开比_，如上一条所描述，对于大量对像的移动是很大开销的，做为老年代的第一选择并不合适。

基于上面的考虑，_老年代一般是由标记清除或者是标记清除与标记整理的混合实现_。以HotSpot中的CMS回收器为例，CMS是基于Mark-Sweep实现的，对于对像的回收效率很高，而对于碎片问题，CMS采用基于Mark-Compact算法的Serial Old回收器做为补偿措施：当内存回收不佳（碎片导致的Concurrent Mode Failure时），将采用Serial Old执行Full GC以达到对老年代内存的整理。

#### 持久代（Perm Gen）

Perm Gen的内存回收默认是关闭的。以由于越多越多的动态技术的使用（Groovy、Cglib、ASM、Drools等）、以及模块化技术。 Perm Gen也可以通过GC实现内存回收。而其对像存活特点与老年代相似（更甚），所以同样可以使用标记清除算法，Hotspot中的CMS回收器就有回收持久代的功能。

### HotSpot算法实现

#### 枚举根节点

在可达性分析中，可以作为GC Roots的节点有很多，但是现在很多应用仅仅方法区就有上百MB，如果逐个检查的话，效率就会变得不可接受。而且，可达性分析必须在一个一致性的快照中进行-即整个分析期间，系统就像冻结了一样。否则如果一边分析，系统一边动态表化，得到的结果就没有准确性。这就导致了系统GC时必须停顿所有的Java执行线程。

目前主流Java虚拟机使用的都是准确式GC，所以当执行系统都停顿下来之后，并不需要一个不漏的检查完所有执行上下文和全局的引用位置，虚拟机应该有办法直接知道哪些地方存放着对象引用。在HotSpot实现中，使用一组称为OopMap的数据结构来达到这个目的。OopMap会在类加载完成的时候，记录对象内什么偏移量上是什么类型的数据，在JIT编译过程中，也会在特定的位置记录下栈和寄存器哪些位置是引用。这样，在GC扫描的时候就可以直接得到这些信息了。(OopMap用于枚举GC Roots; RememberedSet 用于可达性分析)

#### 安全点

可能导致引用关系变化，或者说OopMap内容变化的指令非常多，HotSpot并不会为每条指令都产生OopMap，只是在特定的位置记录了这些信息，这些位置成为“安全点”（SafePoint）。程序执行时只有在达到安全点的时候才停顿开始GC。一般具有较长运行时间的指令才能被选为安全点，如方法调用、循环跳转、异常跳转等。

接下来要考虑的便是，如何在GC时保证所有的线程都“跑”到安全点上停顿下来。这里有两种方案：抢先式中断（Preemptive Suspension）和主动式中断（Voluntary Suspension）。

* 抢先式中断会把所有线程中断，如果某个线程不在安全点上，就恢复让它跑到安全点上。几乎没有虚拟机采用这种方式。
* 主动式中断思想是设立一个GC标志，各个线程会轮询这个标志并在需要时自己中断挂起。这样，标志和安全点是重合的。

#### 安全区域

Safepoint机制可以保证某一程序在运行的时候，在不长的时间里就可以进入GC的Safepoint。但是如果程序没有分配CPU时间，例如处于Sleep状态或者Blocked状态，这时候线程无法响应JVM的中断请求。对于这种情况，只能用安全区域（Safe Region）来解决。

安全区域是指在一段代码片段之中，引用关系不会发生变化。在这个区域中任意地方开始都是安全的。在线程执行到Safe Region中的代码时，就标记自己已经进入了Safe Region，这样JVM在发起GC时就跳过这些线程。在线程要离开Safe Region时，它要检查系统是否已经完成了枚举（或GC过程），如果完成了线程就继续执行，否则就等待。

参考

[JVM垃圾回收算法](http://zsuil.com/?p=88)