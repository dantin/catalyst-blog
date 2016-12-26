---
title: Move Zeroes
date: 2016-10-21 18:31:53
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 283

### 题目

把数组中的0后移动，同时保证元素顺序。

Given an array nums, write a function to move all 0's to the end of it while maintaining the relative order of the non-zero elements.

For example, given nums = [0, 1, 0, 3, 12], after calling your function, nums should be [1, 3, 12, 0, 0].

Note:

1. You must do this in-place without making a copy of the array.
2. Minimize the total number of operations.

### 分析

设置当前指针和哨兵指针，哨兵指针先后移，发现不为零的数字时将数字放入当前指针，哨兵指针移动到数组尾后，将当前指针以后的数字全部置为零。

### 解法

```java
public class Solution {
    public void moveZeroes(int[] nums) {
        int i = 0;
        int seek = 0;
        while(seek < nums.length) {
            if(nums[seek] != 0) {
                nums[i++] = nums[seek];
            }
            seek++;
        }
        for(seek = i; seek < nums.length; seek++) {
            nums[seek] = 0;
        }
    }
}
```