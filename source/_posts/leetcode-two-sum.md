---
title: Two Sum
date: 2016-11-24 11:45:23
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 1

### 题目

找出和为某数的下标。

Given an array of integers, return indices of the two numbers such that they add up to a specific target.

You may assume that each input would have exactly one solution.

__Example__:

```
Given nums = [2, 7, 11, 15], target = 9,

Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1].
```

### 分析

空间换时间，缓存中间结果，注意Double的情况。

### 解法

```java
public class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> cache = new HashMap<Integer, Integer>();
        
        for(int i = 0; i < nums.length; i++) {
            if(cache.containsKey(nums[i]) && i != cache.get(nums[i])) {
                return new int[]{i, cache.get(nums[i])};
            }
            cache.put(target - nums[i], i);
        }
        return null;
    }
}
```