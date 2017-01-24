+++
date = "2017-01-22T15:24:57+08:00"
title = "HashMap的tableSizeFor()"
categories = ["Scholar"]
tags = ["Java", "JDK"]
description = "本文记录Java HashMap的tableSizeFor()方法实现"
slug = "jdk-hashmap-table-size-for"
+++

找出一个数n的最小2的幂次数。

### JDK实现

这部分源码在java.lang.HashMap中。

```java
static final int MAXIMUM_CAPACITY = 1 << 30;

/**
 * Returns a power of two size for the given target capacity.
 */
static final int tableSizeFor(int cap) {
    int n = cap - 1;
    n |= n >>> 1;
    n |= n >>> 2;
    n |= n >>> 4;
    n |= n >>> 8;
    n |= n >>> 16;
    return (n < 0) ? 1 : (n >= MAXIMUM_CAPACITY) ? MAXIMUM_CAPACITY : n + 1;
}
```

被调用的地方

```java
public HashMap(int initialCapacity, float loadFactor) {
    // ...
    this.loadFactor = loadFactor;
    this.threshold = tableSizeFor(initialCapacity);
}
```

当在实例化HashMap实例时，如果给定了initialCapacity，由于HashMap的capacity都是2的幂，因此这个方法用于找到大于等于initialCapacity的最小的2的幂（initialCapacity如果就是2的幂，则返回的还是这个数）。 

### 分析

首先，为什么要对cap做减1操作。`int n = cap - 1`; 

这是为了防止，cap已经是2的幂。如果cap已经是2的幂， 又没有执行这个减1操作，则执行完后面的几条无符号右移操作之后，返回的capacity将是这个cap的2倍。


下面看看这几个无符号右移操作： 

如果n这时为0了（经过了cap-1之后），则经过后面的几次无符号右移依然是0，最后返回的capacity是1（最后有个n+1的操作）。 

这里只讨论n不等于0的情况。 

__第一次右移__

```java
n |= n >>> 1;
```

由于n不等于0，则n的二进制表示中总会有一bit为1，这时考虑最高位的1。通过无符号右移1位，则将最高位的1右移了1位，再做或操作，使得n的二进制表示中与最高位的1紧邻的右边一位也为1，如000011xxxxxx。 

__第二次右移__

```java
n |= n >>> 2;
```

注意，这个n已经经过了`n |= n >>> 1;`操作。假设此时n为000011xxxxxx ，则n无符号右移两位，会将最高位两个连续的1右移两位，然后再与原来的n做或操作，这样n的二进制表示的高位中会有4个连续的1。如00001111xxxxxx。 

__第三次右移__

```java
n |= n >>> 4;
```

这次把已经有的高位中的连续的4个1，右移4位，再做或操作，这样n的二进制表示的高位中会有8个连续的1。如00001111 1111xxxxxx 。

以此类推 

_注意_，容量最大也就是32bit的正数，因此最后`n |= n >>> 16;`，最多也就32个1，但是这时已经大于了MAXIMUM_CAPACITY ，所以取值到MAXIMUM_CAPACITY。

举一个例子说明下吧。 

```console
cap = 10;
n = cap - 1; // 9            0000 1001

n |= n >>> 1;                0000 1001
                             0000 0100   右移1位
                             0000 1101

n |= n >>> 2;                0000 1101
                             0000 0011   右移2位
                             0000 1111

n |= n >>> 4;                0000 1111
                             0000 0000   右移4位
                             0000 1111

n |= n >>> 8;                0000 1111
                             0000 0000   右移8位，无作用
                             0000 1111

n |= n >>> 16;               0000 1111
                             0000 0000   右移16位，无作用
                             0000 1111

n = n + 1;                   0001 0000   得到结果2^4 = 16
```

以上。