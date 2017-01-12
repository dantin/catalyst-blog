+++
date = "2016-11-20T00:05:34+08:00"
title = "Merge Sorted Array"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 88"
slug = "leetcode-merge-sorted-array"
+++

### 题目

合并两个已排好序的数组。

Given two sorted integer arrays nums1 and nums2, merge nums2 into nums1 as one sorted array.

__Note__:

You may assume that nums1 has enough space (size that is greater or equal to m + n) to hold additional elements from nums2. The number of elements initialized in nums1 and nums2 are m and n respectively.

### 分析

从后往前归并，注意边界情况。

边界情况：

1. 数组2（包含数组1同时）为空，直接返回；
2. 数组1为空，把数组2拷贝到数组1中；
3. 归并完成后数组2还有值，把剩下的内容全部拷贝到数组1中；

### 解法

```java
public class Solution {
    public void merge(int[] nums1, int m, int[] nums2, int n) {
        if(n == 0) return;
        if(m == 0) {
            System.arraycopy(nums2, 0, nums1, 0, n);
            return;
        }

        int pos = m + n;
        int i = m - 1;
        int j = n - 1;

        while(i >= 0 && j >= 0 && pos > 0) {
            if(nums1[i] < nums2[j]) {
                nums1[--pos] = nums2[j--];
            } else {
                nums1[--pos] = nums1[i--];
            }
        }
        if(j != -1) System.arraycopy(nums2, 0, nums1, 0, j + 1);
    }
}
```