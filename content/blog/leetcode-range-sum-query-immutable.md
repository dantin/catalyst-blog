+++
date = "2016-11-25T22:31:34+08:00"
title = "Range Sum Query - Immutable"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 303"
slug = "leetcode-range-sum-query-immutable"
+++


Leetcode 303

### 题目

给定整数数组nums，计算下标i与j之间的元素和（i ≤ j），包含边界。

Given an integer array nums, find the sum of the elements between indices i and j (i ≤ j), inclusive.

__Example__:

```
Given nums = [-2, 0, 3, -5, 2, -1]

sumRange(0, 2) -> 1
sumRange(2, 5) -> -1
sumRange(0, 5) -> -3
```

__Note__:

1. You may assume that the array does not change.
2. There are many calls to sumRange function.

### 分析

方法一：

普通做法。

方法二：

空间换时间。

计算辅助数组sums：

```
sums[0] = 0
sums[i+1] = sums[i] + nums[i]
```

### 解法

方法一：

```java
public class NumArray {

    private int[] nums;
    
    public NumArray(int[] nums) {
        this.nums = nums;
    }

    public int sumRange(int i, int j) {
        int sum = 0;
        for(int k = i; k <=j; k++) {
            sum += nums[k];
        }
        return sum;
    }
}


// Your NumArray object will be instantiated and called as such:
// NumArray numArray = new NumArray(nums);
// numArray.sumRange(0, 1);
// numArray.sumRange(1, 2);
```

方法二：

```java
public class NumArray {

    private int[] sums;

    public NumArray(int[] nums) {
        this.sums = new int[nums.length];
        for(int i = 0; i < nums.length; i++) {
            if(i == 0) {
                sums[0] = nums[0];
                continue;
            }
            sums[i] = sums[i-1] + nums[i];
        }
    }

    public int sumRange(int i, int j) {
        if(i == 0) return sums[j];
        return sums[j] - sums[i-1];
    }
}


// Your NumArray object will be instantiated and called as such:
// NumArray numArray = new NumArray(nums);
// numArray.sumRange(0, 1);
// numArray.sumRange(1, 2);
```