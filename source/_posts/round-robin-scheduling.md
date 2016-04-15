title: Round Robin轮询调度算法
date: 2016-04-11 11:15:23
categories: 学术
tags: Algorithm
toc: true
---

本文介绍Round Robin轮询调度算法。

### 轮询调度

轮询调度算法，Round Robin Scheduling，就是以轮询的方式依次将请求调度不同的服务器。其核心是每次调度执行

`i = (i + 1) mod n`

选出第i台服务器。算法的优点是其简洁性，它无需记录当前所有连接的状态，所以它是一种无状态调度。

轮询调度算法的原理是每一次把来自用户的请求轮流分配给内部中的服务器，从1开始，直到N(内部服务器个数)，然后重新开始循环。

### 轮询调度算法流程

假设有一组服务器N台，S = {S1, S2, ... Sn}，一个指示变量i表示上一次选择的服务器ID。变量i被初始化为N-1。一个很经典的算法程序如下：

```python
j = i;
do {
    j = (j + 1) mod n;
    i = j;
    return Si;
} while (j != i);
return NULL;
```

轮询调度算法假设所有服务器的处理性能都相同，不关心每台服务器的当前连接数和响应速度。当请求服务间隔时间变化比较大时，轮询调度算法容易导致服务器间的负载不平衡。

所以此种均衡算法适合于服务器组中的所有服务器都有相同的软硬件配置并且平均服务请求相对均衡的情况。