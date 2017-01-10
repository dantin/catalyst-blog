+++
date = "2016-11-24T11:45:23+08:00"
title = "Two Sum"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 1"
slug = "leetcode-two-sum"
+++

### 题目

找出和为某数的下标。

Given an array of integers, return indices of the two numbers such that they add up to a specific target.

You may assume that each input would have exactly one solution.

__Example__:

```console
Given nums = [2, 7, 11, 15], target = 9,

Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1].
```

### 分析

#### 方法一

暴力解法，$O(n^2)$的复杂度。速度上不符合要求。

#### 方法二

空间换时间，缓存中间结果，注意Double的情况。

```console
Key ＝ target - nums[i]
Value = i
```

* 若num命中，则结果为：$(i, cache[num])$
* 不命中，则缓存当前数据，$cache[num] = i$

特殊情况：$i == cache[num]$

### 解法

Java解法：

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

Python解法：

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