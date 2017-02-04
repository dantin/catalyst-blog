+++
tags = ["Leetcode"]
description = "Leetcode 153"
slug = "leetcode-find-minimum-in-rotated-sorted-array"
date = "2017-01-29T22:27:41+08:00"
title = "Find Minimum in Rotated Sorted Array"
categories = ["Code"]
+++

### 题目

在旋转排序数组中查找最小值。

Suppose an array sorted in ascending order is rotated at some pivot unknown to you beforehand.

(i.e., `0 1 2 4 5 6 7` might become `4 5 6 7 0 1 2`).

Find the minimum element.

You may assume no duplicate exists in the array.

### 分析

__轮询法__

先把第一个元素当作最小元素（记作minVal）。

从左到右遍历数组，如果找到一个比minVal小的值，那它就是真正的最小元素。

如果找不到比minVal更小的值，那么第一个元素就是最小的。

__分治法__

取数组的中间位置的值：

如果它比数组末尾的值大，说明最小元素就位于$[mid + 1, right]$之间。

否则，最小元素一定在$[left, mid]$中。

### 解法

轮询法：

```java
public class Solution {
    public int findMin(int[] nums) {
        int min = nums[0];

        for (int i = 1; i < nums.length; i++) {
            if (nums[i] < min) min = nums[i];
        }
        return min;
    }
}
```

分治法：

```java
public class Solution {
    public int findMin(int[] nums) {
        int left = 0, right = nums.length - 1;
        while (left < right) {
            int mid = (left + right) / 2;
            if (nums[mid] > nums[right]) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        return nums[left];
    }
}
```