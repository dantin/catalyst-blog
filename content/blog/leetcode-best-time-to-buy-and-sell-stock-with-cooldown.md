+++
categories = ["Code"]
tags = ["Leetcode"]
date = "2017-01-19T15:40:42+08:00"
title = "Best Time to Buy and Sell Stock with Cooldown"
description = "Leetcode 309"
slug = "leetcode-best-time-to-buy-and-sell-stock-with-cooldown"
+++

### 题目

找出最优的股票买入卖出时机（但是需要一天的冷却时间）。

Say you have an array for which the $i^\text{th}$ element is the price of a given stock on day $i$.

Design an algorithm to find the maximum profit. You may complete as many transactions as you like (ie, buy one and sell one share of the stock multiple times) with the following restrictions:

* You may not engage in multiple transactions at the same time (ie, you must sell the stock before you buy again).
* After you sell your stock, you cannot buy stock on next day. (ie, cooldown 1 day)

__Example__:

```console
prices = [1, 2, 3, 0, 2]
maxProfit = 3
transactions = [buy, sell, cooldown, buy, sell]
```

### 分析

动态规划，需要维护三个一维数组buy, sell，和rest。其中：

* $buy\[i\]$表示在第$i$天之前最后一个操作是买，此时的最大收益。
* $sell\[i\]$表示在第$i$天之前最后一个操作是卖，此时的最大收益。
* $rest\[i\]$表示在第$i$天之前最后一个操作是冷冻期，此时的最大收益。

则递推式为：

$buy[i]  = max(rest[i-1] - price, buy[i-1])$

$sell[i] = max(buy[i-1] + price, sell[i-1])$

$rest[i] = max(sell[i-1], buy[i-1], rest[i-1])$

上述递推式很好的表示了在买之前有冷冻期，买之前要卖掉之前的股票。

上述递推公式如何保证$[buy, rest, buy]$的情况不会出现呢？

这是由于$buy[i] \le rest[i]$， 即$rest[i] = max(sell[i-1], rest[i-1])$，这保证了$[buy, rest, buy]$不会出现。

另外，由于冷冻期的存在，可以得出$rest[i] = sell[i-1]$。

这样，可以将上面三个递推式精简到两个：

$buy[i]  = max(sell[i-2] - price, buy[i-1])$

$sell[i] = max(buy[i-1] + price, sell[i-1])$

进一步优化，由于$i$只依赖于$i-1$和$i-2$，所以可以在$O(1)$的空间复杂度完成算法。

### 解法

```java
public class Solution {
    public int maxProfit(int[] prices) {
        int buy = Integer.MIN_VALUE, pre_buy = 0, sell = 0, pre_sell = 0;
        for (int price : prices) {
            pre_buy = buy;
            buy = Math.max(pre_sell - price, pre_buy);
            pre_sell = sell;
            sell = Math.max(pre_buy + price, pre_sell);
        }
        return sell;
    }
}
```