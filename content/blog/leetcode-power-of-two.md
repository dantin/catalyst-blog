+++
date = "2016-11-01T10:05:35+08:00"
title = "Power of Two"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 231"
slug = "leetcode-power-of-two"
+++

### 题目

判断一个数是否是2的幂次。

Given an integer, write a function to determine if it is a power of two.

### 分析

2的幂次，二进制就是首位为1，其他位是零。

利用特性$n \land (n - 1) == 0$，求解。

### 解法

```java
public class Solution {
    public boolean isPowerOfTwo(int n) {
        if(n <= 0) return false;
        return (n & (n - 1)) == 0;
    }
}
```