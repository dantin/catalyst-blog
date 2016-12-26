---
title: Two Sum
date: 2016-04-20 23:10:29
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 1

### 题目

给定一个整型数组，找出两个数的下标，使它们的和为目标值。

Given an array of integers, return indices of the two numbers such that they add up to a specific target.

You may assume that each input would have exactly one solution.

Example:

```bash
Given nums = [2, 7, 11, 15], target = 9,

Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1].
```

### 分析

#### 方法一

暴力解法，O(n^2)的复杂度。速度上不符合要求。

#### 方法二

考虑使用Map作为缓存cache：

```bash
Key ＝ target - nums[i]
Value = i
```

* 若num命中，则结果为：`(i, cache[num])`
* 不命中，则缓存当前数据，`cache[num] = i`

特殊情况：`i == cache[num]`

### 答案

#### java

```java
public class TwoSum {

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

#### python

```python
class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        cache = dict()
        for i, num in enumerate(nums):
            if (num in cache.keys()) and (i != cache[num]):
                return [cache[num], i]
            cache[target - num] = i
        return None
```