+++
date = "2016-10-27T13:13:46+08:00"
title = "Contains Duplicate"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 169"
slug = "leetcode-contains-duplicate"
+++

### 题目

判断数组是否包含重复元素。

Given an array of integers, find if the array contains any duplicates. Your function should return true if any value appears at least twice in the array, and it should return false if every element is distinct.

### 分析

遍历并把元素放入集合，发现重复即返回。

### 解法

```java
public class Solution {
    public boolean containsDuplicate(int[] nums) {
        Set<Integer> set = new HashSet<>();
        for(int x : nums) {
            if(set.contains(x)) return true;
            set.add(x);
        }
        return false;
    }
}
```
