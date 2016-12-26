---
title: Number of 1 Bits
date: 2016-11-02 18:19:56
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 191

### 题目

统计任意数字二进制表示中1的个数，即海明码。

Write a function that takes an unsigned integer and returns the number of ’1' bits it has (also known as the [Hamming weight](http://en.wikipedia.org/wiki/Hamming_weight)).

For example, the 32-bit integer ’11' has binary representation:

```
00000000000000000000000000001011
```

so the function should return 3.

### 分析

按位与操作，即可。

### 解法

```java
public class Solution {
    // you need to treat n as an unsigned value
    public int hammingWeight(int n) {
        int sum = 0;
        while(n != 0) {
            sum += n & 1;
            n >>>= 1;
        }
        return sum;
    }
}
```