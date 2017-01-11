+++
date = "2016-10-12T10:40:39+08:00"
title = "The Log Structured Merge Tree"
categories = ["Scholar"]
tags = ["Data Structure"]
description = "本文记录LSM树"
slug = "data-structure-log-structured-merge-tree"
+++

LSM Tree是一种相当优秀的思想。它本身是为了优化B树在更新插入时的性能而被提出来的，所以要彻底理解LSM Tree，就要清楚B树的缺点。

### B+树中的update性能

完全不考虑缓冲的情况下，举例一个可以存储10亿关键字的B树，深度为2，那么每次update事务，至少需要四次IO操作才能完成，三次读，一次写。如果根结点常驻内存的话，最少也需要三次IO。如果是插入（插入也算是update的一种）操作，遇到结点满状态，需要对结点分裂，还需要更多的IO才能完成。

<img src="/images/lsm-b-plus-tree.jpg" alt="B+树的插入问题" style="width: 500px;"/>

即便是到了今天普通PC的磁盘IOPS也就150左右，可以想象，根本无法处理得了大量的并发操作，尤其在海量存储难题面前

### LSM-tree的核心思想

LSM Tree最原始和质朴的思想，就是在内存里对B树的update操作进行缓存。使用cache的做法似乎不值一提，但在当时来说哪怕1MB的闪存价格都非常昂贵，大部分的数据还是通过磁盘来处理，如果你有这方面的经验，就能理解B树这种传统的数据结构实践起来是多么的困难。而且，The Log Structured Merge Tree这篇论文在提出的时候是1996年，当时的内存容量大改在5MB左右。

五分钟法则的由来

五分钟法则是从经济学的角度为降低IT企业运营成本而被提出来的，用术语的话来说，就是COSTp/COSTm，在今天的说法就是，当页面达到每超过300秒就被访问一次的频率后，就应该将这块页面加载到内存以提升性能。而过去的说法，是指页面没有被频繁使用的话，就不应该将其加载到内存中来，87年的今天是5分钟，96年是1分钟，到了今天可能是十几秒。

```console
COSTm = cost of 1 MByte of memory storage
COSTp = disk arm cost to provide 1 page/second I/O rate, for random pages
```

COSTm和COSTp非物理设备的价值那么简单，涉及很多因素，尤其是COSTp，比如Google说，每0.5秒的延迟就会有20%的流量损失，你可以想象一下COSTp值多大。

所以，Patrick O'Neil（LSM论文的作者）们要解决的问题，就是怎么有效利用缓存的策略，Patrick O'Neil的做法是，在内存里维护一个相同的B树，当内存中的B树达到阀值时，然后批量进行rolling merge

<img src="/images/lsm-merge.jpg" alt="LSM Rolling Merge" style="width: 500px;"/>

### NoSQL运动里的LSM实践

NoSQL运动里谈到的LSM相当于复杂的Multi-Component LSM-trees，只是存储组件不再使用B树，而是习惯了另一种更加漂亮的数据结构 Skiplist，Google的Bigtable理论模型里用到的就是这个东西，可以看看levelDB的实现，而且mencached，redis，nessDB等也不乏使用。相比传统的B树，Skiplist最大的特色就是完全平坦化的存储模型，O(logn)的时间复杂度。

LSM与skiplist的结合，带来了一种新的存储架构策略，我自个的话说就是：swap和merge-split

![LSM levelDB](/images/lsm-levelDB.jpg "LSM levelDB")

以levelDB为例，C0是memtable，是内存中的LSM组件，C2 ~ Ck就是sstable，是常驻磁盘的LSM组件，关于存储的设计可以看看这篇文章[KeyValue存储层文件结构的设计]()或者HFile。而C1实质上是sstable在内存中的cache，通常是一个LRU链表。

所谓swap，就是将memtable中的数据直接dump到磁盘形成新的sstable，而meger-split则是删除sstable中过期的数据。这种设计的好处是，无论是插入，更新，还是删除，都可以很轻松的抽象成一个put操作，大大简化了DB的实现逻辑。

![LSM Merge Split](/images/lsm-merge-split.jpg "LSM Merge Split")

但是，这种实现的策略有两个地方限制了其自身可应用的场景，就是update的频率要远大于读取，才能体现出顺序写的性能优势，因为sstable间是无法保证严格有序的，因此查询一个key就不得不在所有的sstable中进行，然后返回最新的数据。用迂回折中的办法，可以对sstable按照timestamp排序，查到最近的一个key并返回。所以bigtable这种模型很可能无法满足精确、实时的海量查询需求。

此外，merge-split还隐藏了另外一个很重要的因素，就是数据文件要达到GB甚至TB级才会有显著的merge-split效果。

要解决这个问题，可以适当改变swap和merge-split的策略。nessDB是个很好的例子。nessDB同样采取LSM的思想，但是不同与上述模型，nessDB确保sstable之间是有序的，对查询操作比较友好。

nessDB是通过牺牲部分写性能来提升查询的效率。memtable在swap的时候并不直接dump成sstable文件，而是合并到现有的sstable文件中去。

### LSM的持久化

如果要确保数据不能丢失，为了应对服务器遇不可抗拒外力因素造成的宕机的情况，通常LSM有两次持久化过程，一次是log，以append形式对所有的update操作先进行日志记录，一旦出现意外情况，即可以恢复log中的内容到memtable，这里实际上相当于重新redo了一系列的事务， 除了增加少量的disk存储开销不会带来其他任何影响。第二次是swap，在memtable达到阀值的时候直接dump到磁盘上形成新的sstable，这个过程叫做最终持久化。

### 总结

LSM的论文洋洋洒洒30多页，其实LSM并不复杂，反而可以说是出奇的简单，Patrick O'Neil在文中列举了很多例子来计算LSM所带来的性能的提升，也许在今天这种情况下是不足论道的，但是Patrick O'Neil迈出了一小步，却是存储难题的一个重大突破。

参考

[Open Open](http://www.open-open.com/lib/view/open1424916275249.html)
[CSDN](http://blog.csdn.net/qq910894904/article/details/38014127)