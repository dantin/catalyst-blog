+++
description = "Leetcode 62"
slug = "leetcode-unique-paths"
date = "2017-01-23T12:30:33+08:00"
title = "Unique Paths"
categories = ["Code"]
tags = ["Leetcode"]
+++

### 题目

求机器人迷宫的所有可能路径。

A robot is located at the top-left corner of a $m \times n$ grid (marked 'Start' in the diagram below).

The robot can only move either down or right at any point in time. The robot is trying to reach the bottom-right corner of the grid (marked 'Finish' in the diagram below).

How many possible unique paths are there?

![机器人迷宫](/images/leetcode_robot_maze.png "Robot Maze")

Above is a $3 \times 7$ grid. How many possible unique paths are there?

_Note_: m and n will be at most 100.

### 分析

__动态规划__

如果机器人要到$(i, j)$这个点，它必须选择先到$(i - 1, j)$或$(i, j - 1)$。即：到$(i, j)$的唯一路径数等于$(i - 1, j)$加上$(i, j - 1)$的个数，所以dp方程:

```console
dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
```

__排列组合__

机器人从第$(1,1)$点走到了第$(m,n)$点。它只能向右或者向下，不管它怎么走，它必然向右走了$m-1$步，向下走了$n-1$步。一共走了$m-1+n-1$步。而不同的走法，本质是向右或者向下构成的$m-1+n-1$长度的序列不同。走法的总数目，本质上是$m-1+n-1$个总步数中选出$m-1$个代表向右走的走法的个数，这个问题的另一种表述是，走法的总数目，本质上是$m-1+n-1$个总步数中选出$n-1$个代表向下走的走法的个数。

这其实正是组合的小性质。

$\dbinom{a}{a+b} = \dbinom{b}{a+b}$

这样题目就转换为了一个数学计算了，求$\dbinom{m-1}{m-1+n-1}$。

### 解法

__动态规划__

```java
public class Solution {
    public int uniquePaths(int m, int n) {
        int[][] dp = new int[m][n];
        for (int i = 0; i < m; i++) {
            dp[i][0] = 1;
        }
        for (int i = 0; i < n; i++) {
            dp[0][i] = 1;
        }

        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
            }
        }
        return dp[m - 1][n - 1];
    }
}
```