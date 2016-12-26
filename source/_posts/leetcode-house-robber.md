---
title: House Robber
date: 2016-11-04 15:09:39
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 198

### 题目

查看最大可能的抢劫数量，不能相邻取。

You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security system connected and __it will automatically contact the police if two adjacent houses were broken into on the same night__.

Given a list of non-negative integers representing the amount of money of each house, determine the maximum amount of money you can rob tonight __without alerting the police__.

### 分析

采用动态规划，通项公式为：

```
Suppose array is from a[0]... a[n]

F(n) = max(F(n-2) + a[n], F(n-1))
```

### 解法

```java
public class Solution {
    public int rob(int[] nums) {
        if(nums == null || nums.length == 0) return 0;
        if(nums.length == 1) return nums[0];
        int res = Math.max(nums[0], nums[1]);
        if(nums.length == 2) return res;

        int hist = nums[0];
        int pre = res;
        for(int i = 2; i < nums.length; i++) {
            res = Math.max(hist + nums[i], pre);
            hist = pre;
            pre = res;
        }

        return Math.max(res, pre);
    }
}
```