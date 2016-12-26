---
title: Remove Duplicates from Sorted Array
date: 2016-11-10 16:09:25
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 26

### 题目

移除有序数组中的重复值，返回长度。

Given a sorted array, remove the duplicates in place such that each element appear only once and return the new length.

Do not allocate extra space for another array, you must do this in place with constant memory.

For example,
Given input array nums = [1,1,2],

Your function should return length = 2, with the first two elements of nums being 1 and 2 respectively. It doesn't matter what you leave beyond the new length.

### 分析

二指针问题。一前一后扫描。

需要注意两者相临时的问题，两个指针一开始不应该重叠！！

### 解法

```java
public class Solution {
    public int removeDuplicates1(int[] nums) {
        if(nums == null || nums.length == 0) return 0;
        if(nums.length == 1) return 1;
        int fast = 1;
        int slow = 0;
        while(fast < nums.length) {
            if(nums[slow] == nums[fast]) {
                fast++;
            } else if(slow + 1 != fast) {
                nums[++slow] = nums[fast++];
            } else {
                slow++;
                fast++;
            }
        }
        return slow+1;
    }
```

优化代码。

```java
public class Solution {
    public int removeDuplicates(int[] nums) {
        if(nums == null || nums.length == 0) return 0;
        if(nums.length == 1) return 1;
        int j = 0;
        for(int i = 1; i < nums.length; i++) {
            if(nums[j] != nums[i]) {
                nums[++j] = nums[i];
            }   
        }
        return j + 1;
    }
}
```