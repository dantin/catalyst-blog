---
title: Remove Element
date: 2016-11-07 17:36:35
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 27

### 题目

移除数组中的目标数值，返回结果数组长度。

Given an array and a value, remove all instances of that value in place and return the new length.

Do not allocate extra space for another array, you must do this in place with constant memory.

The order of elements can be changed. It doesn't matter what you leave beyond the new length.

__Example__:

Given input array nums = [3,2,2,3], val = 3

Your function should return length = 2, with the first two elements of nums being 2.

### 分析

方式两个指针，快指针每次后移，慢指针只在满足条件时后移。

### 解法

```java
public class Solution {
    public int removeElement(int[] nums, int val) {
        int i = 0;
        int len = 0;
        while(i < nums.length) {
            if(nums[i] == val) i++;
            else nums[len++] = nums[i++];
        }
        return len;
    }
}
```