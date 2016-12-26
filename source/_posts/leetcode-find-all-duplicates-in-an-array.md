---
title: Find All Duplicates in an Array
date: 2016-12-22 17:21:55
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 442

### 题目

查找整型数组中的重复元素。

Given an array of integers, 1 ≤ a[i] ≤ n (n = size of array), some elements appear twice and others appear once.

Find all the elements that appear twice in this array.

Could you do it without extra space and in O(n) runtime?

__Example__:

```
Input:
[4,3,2,7,8,2,3,1]

Output:
[2,3]
```

### 分析

排序，保存前一个元素，遍历。

### 解法

```java
public class Solution {
    public List<Integer> findDuplicates(int[] nums) {
        if(nums == null || nums.length == 0) return Collections.emptyList();

        List<Integer> ans = new LinkedList<>();
        
        Arrays.sort(nums);

        int prev = nums[0];
        for(int i = 1; i < nums.length; i++) {
            if(nums[i] == prev) {
                ans.add(nums[i]);
            }
            prev = nums[i];
        }
        return ans;
    }
}
```