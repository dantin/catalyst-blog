+++
date = "2016-12-09T22:21:21+08:00"
title = "Best Time to Buy and Sell Stock II"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 122"
slug = "leetcode-best-time-to-buy-and-sell-stock-ii"
+++


Leetcode 122

### 题目

找出最优的股票买入卖出时机（不限制交易次数，但是任意时段只能有一笔交易）。

Say you have an array for which the ith element is the price of a given stock on day i.

Design an algorithm to find the maximum profit. You may complete as many transactions as you like (ie, buy one and sell one share of the stock multiple times). However, you may not engage in multiple transactions at the same time (ie, you must sell the stock before you buy again).

### 分析

因为不限制交易次数，因此只需要保证当前卖出价比前一次的买入价高，即可。

### 解法

```java
public class Solution {
    public int maxProfit(int[] prices) {
        int sum = 0;
        for(int i = 1; i < prices.length; i++) {
            if(prices[i] > prices[i-1]) {
                sum += prices[i] - prices[i-1];
            }
        }
        return sum;        
    }
}
```