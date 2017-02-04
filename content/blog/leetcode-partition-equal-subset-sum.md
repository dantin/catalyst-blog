+++
description = "Leetcode 416"
slug = "leetcode-partition-equal-subset-sum"
date = "2017-02-04T13:42:55+08:00"
title = "Partition Equal Subset Sum"
categories = ["Code"]
tags = ["Leetcode"]
+++

### 题目

相同子集和分割。

Given a __non-empty__ array containing __only positive integers__, find if the array can be partitioned into two subsets such that the sum of elements in both subsets is equal.

__Note__:

1. Each of the array element will not exceed 100.
2. The array size will not exceed 200.

__Example 1__:

```console
Input: [1, 5, 11, 5]

Output: true

Explanation: The array can be partitioned as [1, 5, 5] and [11].
```

__Example 2__:

```console
Input: [1, 2, 3, 5]

Output: false

Explanation: The array cannot be partitioned into equal sum subsets.
```

### 分析

本问题属于动态规划中的背包问题。

背包问题：假设有$n$个宝石，只有一个容量为$C$的背包，且第$i$个宝石所对应的重量和价值为$w[i]$和$v[i]$,求装哪些宝石可以获得最大的价值收益？

思路：将$n$个宝石进行编号，$0, 1, 2 \dots n-1$，寻找DP的状态和状态转移方程。用$dp[i][j]$表示将前$i$个宝石装到剩余容量为$j$的背包中，那么久很容易得到状态转移方程了。

宝石从0开始编号，所以$dp[i][j]$是在考虑第$i-1$个宝石装包的情况，当然我们要先初始化前0个宝石装包的情况，即$dp[0]=0$,因为不装任何宝石，所以无论如何价值都为0.

$dp[i][j]=Math.max(dp[i-1][j],dp[i-1][j-w[i-1]]+v[i-1])$

* 背包无法再装下第$i-1$个宝石，则：$dp[i-1][j]$;
* 继续将第$i-1$个宝石装包，则：$dp[i-1][j-w[i-1]]+v[i-1]$。

搞清楚了背包问题，这个Partition Equal Subset Sum的题目就迎刃而解了。

1. 判断数组中所有数的和是否为偶数，因为奇数是不可能有解的；
2. 根据背包问题，取前i个数，体积为j，
    $dp[i][j]=Math.max(dp[i-1][j],dp[i-1][j-nums[i-1]]+nums[i-1])$
3. 如果最后$dp[i][nums.length]=sum/2$，返回`true`。

### 解法

```java
public class Solution {
    public boolean canPartition(int[] nums) {
        if (nums == null || nums.length == 0) return false;
        int sum = 0;
        for (int n : nums) {
            sum += n;
        }
        if (sum % 2 == 1) return false;
        sum /= 2;

        int[][] dp = new int[nums.length + 1][sum + 1];
        for (int i = 0; i <= nums.length; i++) {
            for (int j = 0; j <= sum; j++) {
                if (i == 0) {
                    // 前0个数，所以价值均为0；
                    dp[i][j] = 0;
                } else if (j < nums[i - 1]) {
                    // 在装第i-1个数时，先判断剩余容量j是否大于nums[i-1]
                    // 空间不够，所以维持不变
                    dp[i][j] = dp[i - 1][j];
                } else {
                    //空间够，就通过比较大小来判断是否该放入第i-1个数
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i - 1][j - nums[i - 1]] + nums[i - 1]);
                }
            }
        }
        return dp[nums.length][sum] == sum;
    }
}
```