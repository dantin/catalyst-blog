---
title: Missing Number
date: 2016-12-13 22:39:07
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 268

### 题目

找出缺失的数字。

Given an array containing n distinct numbers taken from 0, 1, 2, ..., n, find the one that is missing from the array.

For example,

Given nums = [0, 1, 3] return 2.

__Note__:

Your algorithm should run in linear runtime complexity. Could you implement it using only constant extra space complexity?

### 分析

前n项的和减去数组之和。

通过异或两次等零的性质。

### 解法

解法一：

```java
public class Solution {
    public int missingNumber(int[] nums) {
        int sum = 0;
        for(int i = 0; i < nums.length; i++) {
            sum += i;
            sum -= nums[i];
        }
        sum += nums.length;
        return sum;
    }
}
```

解法二：

```java
public class Solution {
    public int missingNumber(int[] nums) {
        int xor = 0;
        for(int i = 0; i < nums.length; i++) {
            xor ^= i;
            xor ^= nums[i];
        }
        xor ^= nums.length;
        return xor;
    }
}
```