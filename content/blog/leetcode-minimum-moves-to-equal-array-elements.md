+++
date = "2016-11-07T13:58:54+08:00"
title = "Minimum Moves to Equal Array Elements"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 24"
slug = "leetcode-minimum-moves-to-equal-array-elements"
+++

### 题目

给定一个长度为n的非空整数数组，计算最少需要多少次移动可以使所有元素相等，一次移动是指将n - 1个元素加1。

Given a non-empty integer array of size n, find the minimum number of moves required to make all array elements equal, where a move is incrementing n - 1 elements by 1.

__Example__:

```console
Input:
[1,2,3]

Output:
3

Explanation:
Only three moves are needed (remember each move increments two elements):

[1,2,3]  =>  [2,3,3]  =>  [3,4,3]  =>  [4,4,4]
```

### 分析

一次移动将n - 1个元素加1，等价于将剩下的1个元素减1。

因此累加数组中各元素与最小值之差即可。

### 解法

```java
public class Solution {
    public int minMoves(int[] nums) {
        if(nums == null || nums.length == 0) return 0;
        int min = nums[0];
        for(int i = 0; i < nums.length; i++) {
            if(nums[i] < min) min = nums[i];
        }
        int sum = 0;
        for(int i = 0; i < nums.length; i++) {
            sum += nums[i] - min;
        }
        return sum;
    }
}
```