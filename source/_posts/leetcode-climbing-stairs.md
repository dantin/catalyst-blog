---
title: Climbing Stairs
date: 2016-11-02 16:37:26
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 70

### 题目

走阶梯可以走1格或两格，给定一个阶梯的长度n，问有多少种走法。

You are climbing a stair case. It takes n steps to reach to the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

### 分析

类似斐波那契数列，和动规思想，保存前两格的可能走法，递增即可。

### 解法

```java
public class Solution {
    public int climbStairs(int n) {
        if(n <= 0) return 0;
        if(n == 1) return 1;
        if(n == 2) return 2;
        int count = 0;
        int hist = 1;
        int prev = 2;
        for(int i = 3; i <= n; i++) {
            count = hist + prev;
            hist = prev;
            prev = count;
        }
        return count;
    }
}
```