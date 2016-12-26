---
title: 深入理解Java虚拟机之五：垃圾收集器
date: 2016-06-08 15:34:34
categories: 学术
tags: [Java, JVM]
toc: true
---

垃圾收集器是垃圾收集算法的具体实现。Java规范对垃圾收集器的实现没有做任何规定，因此不同的虚拟机提供的垃圾收集器可能有很大差异。HotSpot虚拟机1.6版本使用了多种收集器。

常见的有七种作用于不同分代的收集器，如下图：

![Java垃圾收集器](/images/jvm_garbage_collector.png "Java garbage collector")

* Serial、ParNew、Parallel Scavenge属于新生代收集器；
* CMS、Serial Old（MSC） Parallel Old属于老年代收集器，G1可以作用于这两部分。

相互连线表示收集器可以搭配使用。

### Serial（串行）收集器

Serial收集器是最基本、发展历史最为悠久的收集器。在曾经的JDK1.3之前是新生代收集的唯一选择。

这个收集器是一个单线程的收集器（即只会使用一个CPU或一条收集线程），在它进行垃圾收集的时，必须暂停其他所有的工作线程（Stop The World），直到它收集结束。这个过程是由虚拟机后台发起并自动完成的，在用户不可见的情况下把用户正常的工作线程全部停掉，这对许多应用是无法接受的。下图展示了Serial / Serial Old收集器的运行过程。

![Serial垃圾收集器](/images/jvm_serial_gc.jpg "JVM Serial GC")

为了消除或减少“Stop The World”停顿，从Serial到Parallel收集器，再到Concurrent Mark Sweep（CMS）乃至最新的Garbage First（G1）收集器，越来越复杂，性能也越来越好，用户停顿时间越来越小。

虽然Serial有着这一无法消除的影响，但是它仍旧是虚拟机运行在Client模式下的默认新生代收集器。在单CPU环境来说，Serial由于没有线程交互的开销，专心做垃圾收集，因而具有最高的收集效率。在用户的桌面应用中，分配给虚拟机的内存一般不会很大，收集一两百M的新生代所用的停顿时间完全可以控制在一百ms之内。所以，Serial收集器对于运行在Client模式下的虚拟机来说是一个很好地选择。收集器可用的控制参数如下：
* -XX:+UserSerialGC 在新生代和老年代使用串行收集器
* -XX:+SurvivorRatio 设置eden和survivor区大小的比例
* -XX:+PretenureSizeThreshold 直接晋升到年老代的对象大小，设置此参数后，超过该大小的对象直接在年老代中分配内存
* -XX:+MaxTenuringThreshold 直接晋升到年老代的对象年龄，每个对象在一次Minor GC之后还存活，则年龄加1，当年龄超过该值时进入年老代

### ParNew收集器

ParNew收集器其实就是Serial收集器的多线程版本，除了使用多条线程进行垃圾收集之外，其余行为与Serial收集器一样。但它却是Server模式下的虚拟机中首选的新生代收集器，与性能无关的一个原因是，除了Serial收集器外，只有它能与CMS收集器配合工作，后者是HotSpot 虚拟机中第一款真正意义上的并发（Concurrent）收集器，它第一次实现了让垃圾收集线程与用户线程同时工作。

![ParNew垃圾收集器](/images/jvm_parnew_gc.jpg "Java ParNew GC")

ParNew收集器也是使用`-XX:+UseConcMarkSweepGC`选项后的默认新生代收集器，
也可以使用`-XX:+UseParNewGC`来指定它。

关于垃圾收集中的并发和并行，可以解释如下：

* 并行（Parallel）：指多条垃圾收集线程并行工作，用户线程仍处于等待状态。
* 并发（Concurrent）：指用户线程与垃圾收集线程同时执行。

### Parallel Scavenge 收集器

Parallel Scavenge收集器也是新生代收集器，使用复制算法，又是并行的多线程收集器，和ParNew类似。但是Parallel Scavenge的特点是它的关注点与其他收集器不同，CMS等关注于尽可能缩短用户线程停顿时间，而它目标则是达到一个可控制的吞吐量（Throughput）。所谓吞吐量就是CPU用于运行用户代码的时间与CPU总消耗的时间的比值，如虚拟机运行了100分钟，垃圾收集花掉了1分钟，那么吞吐量便是99%。

* -XX:+UseParNewGC 打开此开关参数后，使用ParNew+Serial Old收集器组合进行垃圾收集。
* -XX:+UseParallelOldGC 打开此开关参数后，使用Parallel Scavenge+Parallel Old收集器组合进行垃圾收集。
* -XX:+ParallelGCThreads 设置并行GC时进行内存回收的线程数。
* -XX:+MaxGCPauseMillis Parallel Scavenge收集器最大GC停顿时间。
* -XX:+GCTimeRation Parallel Scavenge收集器运行时间占总时间比率。
* -XX:+UseAdaptiveSizePolicy Java虚拟机动态自适应策略，动态调整年老代对象年龄和各个区域大小。

### Serial Old收集器

Serial Old收集器是Serial的老年代版本，同样是一个单线程收集器，使用“标记-整理”算法。主要意义也是在Client 模式下使用。

### Parallel Old 收集器

Parallel Old是Parallel Scavenge收集器的老年代版本，使用多线程和“标记-整理”算法。
在它出现之前，由于新生带收集器Paralle Scavenge只能和Serial Old配合，而老年代Serial Old收集器在服务端应用性能上的“拖累”，使用了Parallel Scavenge收集器未必能在整体应用上获得吞吐量最大化的效果。由于Serial Old使用单线程，无法充分利用服务器的CPU资源，这种组合甚至不如ParNew+CMS的组合给力。直到Parallel Old的出现。Parallel Old工作过程如下图。

![Parallel Scavenge/Old收集器](/images/jvm_parallel_scavenge.jpg "Java Parallel Scavenge/Old GC")

### CMS收集器
CMS(Concurrent Mark Sweep)收集器是一种以获取最短回收停顿时间为目标的收集器。主要用于互联网或B/S系统的服务端，这类应用尤其重视服务的响应速度。

从名字可以看出，CMS是基于“标记-清除”算法的，运作过程更加复杂一些，分为4个步骤：

1. 初始标记(CMS initial mark)   标记GC Roots直接关联的对象
2. 并发标记(CMS concurrenr mark)   可达性分析算法
3. 重新标记(CMS remark)  并发变动修改
4. 并发清除(CMS concurrent sweep）

其中初始标记、重新标记这两个步骤任然需要停顿其他用户线程。初始标记仅仅只是标记出GC ROOTS能直接关联到的对象，速度很快，并发标记阶段是进行GC ROOTS根搜索算法阶段，会判定对象是否存活。而重新标记阶段则是为了修正并发标记期间，因用户程序继续运行而导致标记产生变动的那一部分对象的标记记录，这个阶段的停顿时间会比初始标记阶段稍长，但比并发标记阶段要短。由于整个过程中耗时最长的并发标记和并发清除过程中，收集器线程都可以与用户线程一起工作，所以整体来说，CMS收集器的内存回收过程是与用户线程一起并发执行的。执行过程如下图。

![CMS收集器](/images/jvm_cms.jpg "Java CMS GC")

CMS收集器的优点：并发收集、低停顿，但是CMS还远远达不到完美，主要有三个显著缺点：

* CMS收集器对CPU资源非常敏感。在并发阶段，虽然不会导致用户线程停顿，但是会占用CPU资源而导致引用程序变慢，总吞吐量下降。CMS默认启动的回收线程数是：(CPU数量+3) / 4。
* CMS收集器无法处理浮动垃圾，可能出现“Concurrent Mode Failure“，失败后而导致另一次Full GC的产生。由于CMS并发清理阶段用户线程还在运行，伴随程序的运行自热会有新的垃圾不断产生，这一部分垃圾出现在标记过程之后，CMS无法在本次收集中处理它们，只好留待下一次GC时将其清理掉。这一部分垃圾称为“浮动垃圾”。也是由于在垃圾收集阶段用户线程还需要运行，即需要预留足够的内存空间给用户线程使用，因此CMS收集器不能像其他收集器那样等到老年代几乎完全被填满了再进行收集，需要预留一部分内存空间提供并发收集时的程序运作使用。在默认设置下，CMS收集器在老年代使用了68%的空间时就会被激活，也可以通过参数-XX:CMSInitiatingOccupancyFraction的值来提供触发百分比，以降低内存回收次数提高性能。要是CMS运行期间预留的内存无法满足程序其他线程需要，就会出现“Concurrent Mode Failure”失败，这时候虚拟机将启动后备预案：临时启用Serial Old收集器来重新进行老年代的垃圾收集，这样停顿时间就很长了。所以说参数-XX:CMSInitiatingOccupancyFraction设置的过高将会很容易导致“Concurrent Mode Failure”失败，性能反而降低。
* 最后一个缺点，CMS是基于“标记-清除”算法实现的收集器，使用“标记-清除”算法收集后，会产生大量碎片。空间碎片太多时，将会给对象分配带来很多麻烦，比如说大对象，内存空间找不到连续的空间来分配不得不提前触发一次Full GC。为了解决这个问题，CMS收集器提供了一个-XX:UseCMSCompactAtFullCollection开关参数，用于在Full GC之后增加一个碎片整理过程，还可通过-XX:CMSFullGCBeforeCompaction参数设置执行多少次不压缩的Full GC之后，跟着来一次碎片整理过程。

### G1收集器

G1是面向服务端应用的垃圾收集器。具有如下几个特点。

* 并行与并发：G1能充分利用多CPU、多核环境下的硬件优势，使用多个CPU（CPU或者CPU核心）来缩短Stop-The-World停顿的时间，部分其他收集器原本需要停顿Java线程执行的GC动作，G1收集器仍然可以通过并发的方式让Java程序继续执行。
* 分代收集：与其他收集器一样，分代概念在G1中依然得以保留。虽然G1可以不需其他收集器配合就能独立管理整个GC堆，但它能够采用不同的方式去处理新创建的对象和已经存活了一段时间、熬过多次GC的旧对象以获取更好的收集效果。
* 空间整合：与CMS的“标记-清理”算法不同，G1从整体看来是基于“标记-整理”算法实现的收集器，从局部（两个Region之间）上看是基于“复制”算法实现，无论如何，这两种算法都意味着G1运作期间不会产生内存空间碎片，收集后能提供规整的可用内存。这种特性有利于程序长时间运行，分配大对象时不会因为无法找到连续内存空间而提前触发下一次GC。
* 可预测的停顿：这是G1相对于CMS的另外一大优势，降低停顿时间是G1和CMS共同的关注点，但G1除了追求低停顿外，还能建立可预测的停顿时间模型，能让使用者明确指定在一个长度为M毫秒的时间片段内，消耗在垃圾收集上的时间不得超过N毫秒，这几乎已经是实时Java（RTSJ）的垃圾收集器特征了。

使用G1收集器时，Java堆的内存布局与就与其他收集器有很大差别，它将整个Java堆划分为多个大小相等的独立区域（Region），虽然还保留有新生代和老年代的概念，但新生代和老年代不再是物理隔离的了，它们都是一部分Region（不需要连续）的集合。

![JVM Hotspot Heap Structure](/images/jvm_hotspot_heap_structure.png "JVM Hotspot Heap Structure")

![JVM G1 Heap Allocation](/images/jvm_g1_heap_allocation.png "JVM G1 Heap Allocation")

G1收集器之所以能建立可预测的停顿时间模型，是因为它可以有计划地避免在整个Java堆中进行全区域的垃圾收集。G1跟踪各个Region里面的垃圾堆积的价值大小（回收所获得的空间大小以及回收所需时间的经验值），在后台维护一个优先列表，每次根据允许的收集时间，优先回价值最大的Region（这也就是Garbage-First名称的来由）。这种使用Region划分内存空间以及有优先级的区域回收方式，保证了G1收集器在有限的时间内获可以获取尽可能高的收集效率。

G1收集器的运作大致可划分为以下几个步骤： 

* 初始标记（Initial Marking）
* 并发标记（Concurrent Marking）
* 最终标记（Final Marking）
* 筛选回收（Live Data Counting and Evacuation）

详细可参考[CSDN](http://blog.csdn.net/renfufei/article/details/41897113)和[Java Eye](http://alaric.iteye.com/blog/2264919)