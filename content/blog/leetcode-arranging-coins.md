+++
date = "2016-10-31T18:46:17+08:00"
title = "Arranging Coins"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 441"
slug = "leetcode-arranging-coins"
+++

### 题目

排列硬币。

You have a total of n coins that you want to form in a staircase shape, where every k-th row must have exactly k coins.

Given _n_, find the total number of __full__ staircase rows that can be formed.

n is a non-negative integer and fits within the range of a 32-bit signed integer.

__Example 1__:

```console
n = 5

The coins can form the following rows:
¤
¤ ¤
¤ ¤

Because the 3rd row is incomplete, we return 2.
```

__Example 2__:

```console
n = 8

The coins can form the following rows:
¤
¤ ¤
¤ ¤ ¤
¤ ¤

Because the 4th row is incomplete, we return 3.
```

### 分析

题目不难，但是需要注意数字越界，尤其是是用公式

$sum = n * (n + 1) / 2$


所以，这里直接递减，确保不越界。

### 解法

```java
public class Solution {
    public int arrangeCoins(int n) {
        int i = 0;
        while(true) {
            n -= i;
            if(n <= i) {
                break;
            }
            i++;
        }
        return i;
    }
}
```