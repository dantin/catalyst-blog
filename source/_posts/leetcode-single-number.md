---
title: Single Number
date: 2016-10-19 22:37:57
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 136

### 题目

一个数组，里面的元素除了一个意外其他都是成对出现的，找出那个特殊的元素 (时间复杂度O(n)，不用多余的变量)。

Given an array of integers, every element appears twice except for one. Find that single one.

__Note:__

Your algorithm should have a linear runtime complexity. Could you implement it without using extra memory?

### 分析

异或的特性是，A xor A = 0，利用这个特性，可以找出此题的解法。

### 解法

```java
public class Solution {
    public int singleNumber(int[] nums) {
        int target = 0;
        for(int i = 0; i < nums.length; i++) {
            target ^= nums[i];
        }
        return target;
    }
}
```