---
title: Minimum Moves to Equal Array Elements II
date: 2016-12-04 23:02:57
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 413

### 题目

给定一个长度为n的非空整数数组，计算最少需要多少次移动可以使所有元素相等，一次移动是指将某一元素加1或减1。

Given a __non-empty__ integer array, find the minimum number of moves required to make all array elements equal, where a move is incrementing a selected element by 1 or decrementing a selected element by 1.

You may assume the array's length is at most 10,000.

__Example__:

```
Input:
[1,2,3]

Output:
2

Explanation:
Only two moves are needed (remember each move increments or decrements one element):

[1,2,3]  =>  [2,2,3]  =>  [2,2,2]
```

### 分析

求数组各元素与中位数差的绝对值之和。

### 解法

```java
public class Solution {
    public int minMoves2(int[] nums) {
        Arrays.sort(nums);
        int mid = nums[nums.length/2];
        int sum = 0;
        for(int x : nums) {
            sum += Math.abs(x - mid);
        }
        return sum;
    }
}
```