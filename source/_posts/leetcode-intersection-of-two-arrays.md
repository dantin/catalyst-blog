---
title: Intersection of Two Arrays
date: 2016-10-24 10:46:43
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 349

### 题目

求两个数组的交集。

Given two arrays, write a function to compute their intersection.

Example:
Given nums1 = [1, 2, 2, 1], nums2 = [2, 2], return [2].

Note:
Each element in the result must be unique.
The result can be in any order.

### 分析

构造集合，求交集。时间复杂度O(n * log(n))。

### 解法

```java
public class Solution {
    public int[] intersection(int[] nums1, int[] nums2) {
        Set<Integer> set1 = IntStream.of(nums1).boxed().collect(Collectors.toSet());
        Set<Integer> set2 = IntStream.of(nums2).boxed().collect(Collectors.toSet());
        set1.retainAll(set2);
        
        return set1.stream().mapToInt(Integer::intValue).toArray();
    }
}
```