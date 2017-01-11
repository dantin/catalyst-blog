+++
date = "2017-01-03T10:55:14+08:00"
title = "House Robber II"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 213"
slug = "leetcode-house-robber-ii"
+++

### 题目

升级版的[House Robber](/2016/11/04/leetcode-house-robber/)，现在头尾成环，求最大可能的抢劫数量，不能相邻取。

__Note__: This is an extension of [House Robber](/2016/11/04/leetcode-house-robber/).

After robbing those houses on that street, the thief has found himself a new place for his thievery so that he will not get too much attention. This time, all houses at this place are __arranged in a circle__. That means the first house is the neighbor of the last one. Meanwhile, the security system for these houses remain the same as for those in the previous street.

Given a list of non-negative integers representing the amount of money of each house, determine the maximum amount of money you can rob tonight __without alerting the police__.

### 分析

参考[House Robber](/2016/11/04/leetcode-house-robber/)中的动态规划解法。

把第一家和最后一家分别去掉，各算一遍能抢的最大值，然后比较两个值取其中较大的一个即可。

### 解法

```java
public class Solution {
    public int rob(int[] nums) {
        if (nums.length <= 1) return nums.length == 0 ? 0 : nums[0];

        return Math.max(rob(nums, 0, nums.length - 1), rob(nums, 1, nums.length));
    }
    
    private int rob(int[] nums, int left, int right) {
        int ans = 0;
        int pre = 0, hist = 0;
        for (int i = left; i < right; i++) {
            ans = Math.max(hist + nums[i], pre);
            hist = pre;
            pre = ans;
        }
        return Math.max(ans, pre);
    }
}
```