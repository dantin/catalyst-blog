+++
tags = ["Leetcode"]
description = "Leetcode 35"
slug = "leetcode-search-insert-position"
categories = ["Code"]
date = "2017-01-25T14:58:47+08:00"
title = "Search Insert Position"
+++

### 题目

搜索数字应该插入的位置。

Given a sorted array and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.

You may assume no duplicates in the array.

Here are few examples.

* $[1,3,5,6]$, 5 → 2
* $[1,3,5,6]$, 2 → 1
* $[1,3,5,6]$, 7 → 4
* $[1,3,5,6]$, 0 → 0

### 分析

类似二分查找的思路。

当查找的target不在list中时，返回该target应在此list中插入的位置。 

当循环结束时，如果没有找到target，那么low一定停target应该插入的位置上，high一定停在恰好比target小的index上。如：

```console
[1,3,5,6], 7
```

过程如下：

```console
low = 0, high = 3

step1: 
    mid = 1
    A[mid] = 3, 3<7

    low = mid + 1 = 2

low = 2, high = 3

step2:
    mid = 2
    A[mid] = 5, 5<7

    low = mid + 1 = 3


low = 3, high = 3

step3:
    mid = 3
    A[mid] = 6, 6<7

    low = mid + 1 = 4 

low = 4, high = 3

return low = 4; 
```

### 解法

递归：

```java
public class Solution {
    public int searchInsert(int[] nums, int target) {
        if (nums == null || nums.length == 0) return 0;
        int low = 0, high = nums.length - 1;

        while (low <= high) {
            int mid = (low + high) / 2;

            if (nums[mid] > target) {
                high = mid - 1;
            } else if (nums[mid] < target) {
                low = mid + 1;
            } else {
                return mid;
            }

        }
        return low;
    }
}
```
