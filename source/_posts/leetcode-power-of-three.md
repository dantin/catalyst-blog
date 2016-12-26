---
title: Power of Three
date: 2016-11-01 09:45:43
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 326

### 题目

判断一个数是否是3的幂次。

Given an integer, write a function to determine if it is a power of three.

__Follow up__:

Could you do it without using any loop / recursion?

### 分析

直接用3除，如果最后余0，则可确认是3的幂次。

考虑用`lg(n) / lg(3)`，判断是否可以整除。

考虑`1162261467 % n`是否为零，其中`1162261467`是int中最大的3次幂。

### 解法

```java
public class Solution {
    public boolean isPowerOfThree(int n) {
        if(n <= 0) return false;
        return 1162261467 % n == 0;
    }
}
```