+++
date = "2017-02-08T10:45:20+08:00"
title = "Minimum Path Sum"
description = "Leetcode 64"
slug = "leetcode-minimum-path-sum"
categories = ["Code"]
tags = ["Leetcode"]
+++

### 题目

找出缺失的数字。

Given a $m \times n$ grid filled with non-negative numbers, find a path from top left to bottom right which minimizes the sum of all numbers along its path.

__Note__: You can only move either down or right at any point in time.

### 分析

动态规划

路径只可能来自于左边或者上边。即：

```console
dp[x, y] = min(dp[x-1, y], dp[x, y-1]) + a[x, y] # 其中a[x, y]是棋盘中(x, y)点的权重取值。
```

然后考虑位于最左边一列与左上边的一行，得到所有的状态转移方程为：

* 第一列：$dp(i, 0) = \sum_{k=1}^i grid[k][0]$
* 第一行：$dp(0, j) = \sum_{k=1}^j grid[0][k]$
* 其他行：$dp(i, j) = min(dp(i-1, j), dp(i, j-1)) + grid[i][j]$

### 解法

```java
public class Solution {
    public int minPathSum(int[][] grid) {
        int row = grid.length;
        int col = grid[0].length;
        int[][] dp = new int[row][col];
        dp[0][0] = grid[0][0];
        for (int i = 1; i < row; i++)
            dp[i][0] = dp[i - 1][0] + grid[i][0];
        for (int j = 1; j < col; j++)
            dp[0][j] = dp[0][j - 1] + grid[0][j];
        for (int i = 1; i < row; i++) {
            for (int j = 1; j < col; j++) {
                dp[i][j] = Math.min(dp[i - 1][j], dp[i][j - 1]) + grid[i][j];
            }
        }
        return dp[row - 1][col - 1];
    }
}
```