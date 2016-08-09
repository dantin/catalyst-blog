---
title: Timsort排序算法
date: 2016-08-09 14:25:25
categories: 学术
tags: Algorithm
toc: true
---

TimSort排序是一种优化的归并排序，它将归并排序(merge sort) 与插入排序(insertion sort) 结合，并进行了一些优化。对于已经部分排序的数组，时间复杂度远低于 O(n log(n))，最好可达 O(n)，对于随机排序的数组，时间复杂度为 O(nlog(n))，平均时间复杂度 O(nlog(n))。

### 概述

它的整体思路是这样的：

1. 遍历数组，将数组分为若干个升序或降序的片段，（如果是降序片段，反转降序的片段使其变为升序），每个片段称为一个Runtask
2. 从数组中取一个RunTask，将这个RunTask压栈。
3. 取出栈中相邻两个的RunTask，做归并排序，并将结果重新压栈。
4. 重复(2),(3)过程，直到所有数据处理完毕。
这篇文章就不再过多的阐述Timsort整体思路了，有兴趣可以参考[理解timsort, 第一部分：适应性归并排序(Adaptive Mergesort)](http://blog.kongfy.com/2012/10/%E8%AF%91%E7%90%86%E8%A7%A3timsort-%E7%AC%AC%E4%B8%80%E9%83%A8%E5%88%86%EF%BC%9A%E9%80%82%E5%BA%94%E6%80%A7%E5%BD%92%E5%B9%B6%E6%8E%92%E5%BA%8Fadaptive-mergesort/)

### Timsort的归并

重点说一下Timsort中的归并。归并过程相对普通的归并排序做了一定的优化，假如有如下的一段数组：

![输入数组](/images/timsort-001.png "Timsort-001")

#### 拆分RunTask

第一步，首先把数组拆成两个RunTask，这里称为A段和B段，注意，A段和B段在物理地址上是连续的：

![拆分成RunTask](/images/timsort-002.png "Timsort-002")

#### 掐头去尾

第二步，A段的起点为base1，剩余元素数量为len1；B段起点为base2，剩余元素数量为len2。取B点的起点值B[base2]，在A段中进行二分查找，将A段中小于等于B[base2]的段作为merge结果的起始部分；再取A段的终点值a[base1 + len1 – 1]，在B段中二分查找，将B段中大于等于a[base1 + len1 – 1]值的段作为结果的结束部分。

更形象的说，这里把待归并的数据“掐头去尾”，只需要合并中间的数据就可以了：

![掐头去尾](/images/timsort-003.png "Timsort-003")

#### 生成tmp数组

第三步，需要创建一个tmp数组，大小为B段截取后的大小，并把B段剩余的数据拷贝过去，因为合并过程中这些数据会被覆盖掉。

程序会记录corsor1和corsor2，这是待归并数据的指针，初始位置在A段和tmp段的末尾。同时会记录合并后数组的dest指针，位置在原B段的末尾。

这里还有一个小优化：生成dest指针时会直接把A段cursor1指向的数据拷贝到B段末尾，同时cursor–,dest–。因为之前(2)步的时候已经保证了arr[cursor1]>arr[dest]

![创建tmp数组](/images/timsort-004.png "Timsort-004")

#### 归并

第四步，进行归并排序，这里每次归并比较时会记录A和tmp段比较“胜利（大于对方）”的次数，比较失败（小于对方）时会把胜利数清零。当有一个段的数据连续N次胜利时会激活另一个优化策略，在这里假设N为4，下图已经是A段连续胜利了4次的情况：

![归并排序](/images/timsort-005.png "Timsort-005")

#### 自适应优化

第五步，优化策略，如果连续胜利N次，那么可以假设A段的数据平均大于B段，此时会用tmp[cursor2]的值在A[base0]至A[cursor1]中查找第一个小于tmp[cursor2]的索引k，并把A[k+1]到A[cursor1]的数据直接搬移到A[dest-len,dest]。

对于例子中的数据，tmp[cursor2]=8，在A数组中查找到小于8的第一个索引（-1），之后把A[0,1]填充到A[dest-1,dest]，cursor1和dest指针左移两个位置。

![优化策略](/images/timsort-006.png "Timsort-006")

#### 情况一

第六步，如果cursor1>=0，之后会再用curosr1指向的数据在tmp数组中查找，由于这里cursor1已经是-1了，循环结束。

#### 情况二

第七步，拷贝，最后把tmp里剩余的数据拷贝到A数组的剩余位置中，结束。

![拷贝](/images/timsort-007.png "Timsort-007")

参考：[AXB的自我修养](http://blog.2baxb.me/archives/993)
