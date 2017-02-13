+++
slug = "leetcode-longest-increasing-subsequence"
date = "2017-02-09T15:05:31+08:00"
title = "Longest Increasing Subsequence"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 300"
+++

### 题目

最长递增子串。

Given an unsorted array of integers, find the length of longest increasing subsequence.

For example,

Given $[10, 9, 2, 5, 3, 7, 101, 18]$,

The longest increasing subsequence is $[2, 3, 7, 101]$, therefore the length is `4`. Note that there may be more than one LIS combination, it is only necessary for you to return the length.

Your algorithm should run in $O(n^2)$ complexity.

__Follow up__: Could you improve it to $O(n \log n)$ time complexity?

### 分析

动态规划。

因为子序列要求是递增的，所以重点是子序列的起始字符和结尾字符，因此我们可以利用结尾字符。想到：以$A\[0\]$结尾的最长递增子序列有多长？以$A\[1\]$结尾的最长递增子序列有多长？... 以$A\[n-1\]$结尾的最长递增子序列有多长？

分析如下图所示：

| 内容  |  |||||||
|:-----:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Array | 1 | 4 | 6 | 2 | 8 | 9 | 7 |
| LIS   | 1 | 2 | 3 | 2 | 4 | 5 | 4 |

所以，我们可以使用一个额外的空间来保存前面已经算得的最长递增子序列，然后每次更新当前的即可。也就是问题演化成：已经计算得到了$b[0,1,2,\dots,i-1]$，如何计算得到$b\[i\]$呢？

显然，如果$a_i>=a_j$，则可以将$a_i$放到$b\[j\]$的后面，得到比$b\[j\]$更长的子序列。从而：

```console
b[i] = max{b[j]}+1, When A[i] > A[j] && 0 <= j < i.
```

所以计算$b\[i\]$的过程是，遍历$b\[i\]$之前的所有位置j，找出满足关系式的最大的$b\[j\]$.

得到$b[0\dots n-1]$之后，遍历所有的$b\[i\]$找到最大值，即为最大递增子序列。 总的时间复杂度为$O(N^2)$。

### 解法

```java
public class Solution {
    public int lengthOfLIS(int[] nums) {
        if (nums == null || nums.length == 0) return 0;
        int[] dp = new int[nums.length];
        dp[0] = 1;
        int ans = 1;
        for (int i = 1; i < nums.length; i++) {
            int max = 0;
            for (int j = 0; j < i; j++) {
                if (nums[j] < nums[i] && dp[j] > max) {
                    max = dp[j];
                }
            }
            dp[i] = max + 1;
            ans = Math.max(dp[i], ans);
        }

        return ans;
    }
}
```