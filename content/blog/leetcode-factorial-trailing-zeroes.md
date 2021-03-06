+++
date = "2016-11-10T17:03:33+08:00"
title = "Factorial Trailing Zeroes"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 172"
slug = "leetcode-factorial-trailing-zeroes"
+++

### 题目

判断阶乘结果有多少个零。

Given an integer n, return the number of trailing zeroes in n!.

__Note__: Your solution should be in logarithmic time complexity.

### 分析

阶乘结果中零的数量取决于里面有多少个5（2的个数肯定大于5的个数）。

$25, 125 \dots$分别有2个5，3个5.

考虑到可能会溢出，尽量减少结果。

### 解法

```java
public class Solution {
    public int trailingZeroes(int n) {
        int sum = 0;
        while(n > 0) {
            sum += n / 5;
            n /= 5;
        }
        return sum;
    }
}
```