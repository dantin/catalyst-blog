+++
date = "2016-11-02T16:14:09+08:00"
title = "Best Time to Buy and Sell Stock"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 121"
slug = "leetcode-best-time-to-buy-and-sell-stock"
+++

### 题目

找出最优的股票买入卖出时机。

Say you have an array for which the _i(th)_ element is the price of a given stock on day _i_.

If you were only permitted to complete at most one transaction (ie, buy one and sell one share of the stock), design an algorithm to find the maximum profit.

__Example 1__:

```console
Input: [7, 1, 5, 3, 6, 4]
Output: 5

max. difference = 6-1 = 5 (not 7-1 = 6, as selling price needs to be larger than buying price)
```

__Example 2__:

```console
Input: [7, 6, 4, 3, 1]
Output: 0

In this case, no transaction is done, i.e. max profit = 0.
```

### 分析

最简单的做法是用两层循环，找出差值最大的树，时间复杂度O(n^2)。

优化后，使用动态规划，保存前一个状态最小值、前一个状态的最佳买入时机，后续推导即可。

### 解法

```java
public class Solution {
    public int maxProfit(int[] prices) {
        if(prices == null || prices.length == 0) return 0;
        int min = prices[0];
        int current = 0;
        int prev = 0;
        for(int i = 1; i < prices.length; i++) {
            int n = prices[i];
            current = (n - min > prev) ? (n - min) : prev;
            if(n < min) min = n;
            prev = current;
        }
        return current;
    }
}
```