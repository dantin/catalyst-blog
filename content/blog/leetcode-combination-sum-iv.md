+++
date = "2016-12-31T21:50:26+08:00"
title = "Combination Sum IV"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 377"
slug = "leetcode-combination-sum-iv"
+++


Leetcode 377

### 题目

给定一个元素互不相同且均为正数的数组，有多少种办法可以用该数组中的数组合成target（可以重复使用）。

Given an integer array with all positive numbers and no duplicates, find the number of possible combinations that add up to a positive integer target.

__Example__:

```console
nums = [1, 2, 3]
target = 4

The possible combination ways are:
(1, 1, 1, 1)
(1, 1, 2)
(1, 2, 1)
(1, 3)
(2, 1, 1)
(2, 2)
(3, 1)

Note that different sequences are counted as different combinations.

Therefore the output is 7.
```

__Follow up__:

* What if negative numbers are allowed in the given array?
* How does it change the problem?
* What limitation we need to add to the question to allow negative numbers?

### 分析

动态规划

递推公式：$dp[i] = \sum\limits_{j=0}^{i-1} dp[j]$，其中：$i-j \in nums$

### 解法

```java
public class Solution {
    public int combinationSum4(int[] nums, int target) {
        int[] dp = new int[target + 1];
        dp[0] = 1;
        for (int i = 1; i < dp.length; i++) {
            for (int n : nums) {
                if (i >= n) dp[i] += dp[i - n];
            }
        }
        return dp[target];
    }
}
```
