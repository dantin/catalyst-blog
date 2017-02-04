+++
date = "2017-02-02T22:00:21+08:00"
title = "Increasing Triplet Subsequence"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 334"
slug = "leetcode-increasing-triplet-subsequence"
+++

### 题目

求一个无序数组中是否有任意三个数字是递增关系的。

Given an unsorted array return whether an increasing subsequence of length 3 exists or not in the array.

Formally the function should:

> Return true if there exists $i, j, k$ 
>
> such that $arr[i] < arr[j] < arr[k]$ given $0 ≤ i < j < k ≤ n-1$ else return false.

Your algorithm should run in $O(n)$ time complexity and $O(1)$ space complexity.

__Examples__:

Given $[1, 2, 3, 4, 5]$,
return `true`.

Given $[5, 4, 3, 2, 1]$,
return `false`.

### 分析

__动态规划__

用一个$dp$数组，$dp[i]$表示在$i$位置之前小于等于$nums[i]$的数字的个数(包括其本身)。

初始化$dp$数组都为1，然后开始遍历原数组，对当前数字$nums[i]$，遍历其之前的所有数字，如果之前某个数字$nums[j]$小于$nums[i]$，那么我们更新$dp[i] = max(dp[i], dp[j] + 1)$，如果此时$dp[i]$到3了，则返回`true`，若遍历完成，则返回`false`

__遍历法__

遍历数组，维护一个最小值，和倒数第二小值，遍历原数组的时候，如果当前数字小于等于最小值，更新最小值，如果小于等于倒数第二小值，更新倒数第二小值，如果当前数字比最小值和倒数第二小值都大，说明此时有三个递增的子序列了，直接返回`ture`，否则遍历结束返回`false`

### 解法

__动态规划__

```java
public class Solution {
    public boolean increasingTriplet(int[] nums) {
        if (nums == null || nums.length == 0) return false;
        int[] dp = new int[nums.length];
        for (int i = 0; i < nums.length; i++) {
            dp[i] = 1;
        }
        dp[0] = 1;
        for (int i = 0; i < nums.length; i++) {
            for (int j = 0; j < i; j++) {
                if (nums[j] < nums[i]) {
                    dp[i] = Math.max(dp[i], dp[j] + 1);
                    if (dp[i] >= 3) return true;
                }
            }
        }
        return false;
    }
}
```

__遍历法__

```java
public class Solution {
    public boolean increasingTriplet(int[] nums) {
        int min1 = Integer.MAX_VALUE, min2 = Integer.MAX_VALUE;

        for (int x : nums) {
            if (min1 >= x) min1 = x;
            else if (min2 >= x) min2 = x;
            else return true;
        }

        return false;
    }
}
```