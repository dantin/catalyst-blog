+++
date = "2016-12-11T22:46:09+08:00"
title = "Count Numbers with Unique Digits"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 357"
slug = "leetcode-count-numbers-with-unique-digits"
+++

### 题目

给定非负的整数n，求在$0 ≤ x < 10n$中，有多少每个位上的数字互不相同的数？

如$n =2$时，范围为$[0,100]$，共有91个数（除了11,22,33,44,55,66,77,88,99）

Given a non-negative integer n, count all numbers with unique digits, x, where 0 ≤ x < 10n.

__Example__:

Given n = 2, return 91. (The answer should be the total numbers in the range of 0 ≤ x < 100, excluding $[11,22,33,44,55,66,77,88,99]$)

Hint:

* A direct way is to use the backtracking approach.
* Backtracking should contains three states which are (the current number, number of steps to get that number and a bitmask which represent which number is marked as visited so far in the current number). Start with state (0,0,0) and count all valid number till we reach number of steps equals to 10n.
* This problem can also be solved using a dynamic programming approach and some knowledge of combinatorics.
* Let f(k) = count of numbers with unique digits with length equals k.
* $f(1) = 10, ..., f(k) = 9 * 9 * 8 * ... (9 - k + 2)$ The first factor is 9 because a number cannot start with $0$.

### 分析

排列组合。

设i为长度为i的各个位置上数字互不相同的数。

```console
i==1 : 1 0（0~9共10个数，均不重复）
i==2: 9 * 9 （第一个位置上除0外有9种选择，第2个位置上除第一个已经选择的数，还包括数字0，也有9种选择）
i ==3: 9* 9 * 8 （前面两个位置同i==2，第三个位置除前两个位置已经选择的数还有8个数可以用）
...
i== n: 9 * 9 * 8 *…… (9-i+2)

```

若$9-i+2>0$，即$i<11$，也就是i最大为10。

### 解法

```java
public class Solution {
    public int countNumbersWithUniqueDigits(int n) {
        n = Math.min(n, 10);
        int[] dp = new int[n + 1];
        dp[0] = 1;
        for(int i = 1; i <= n; i++) {
            dp[i] = 9;
            for(int j = 9; j >= 9 - i + 2; j--) {
                dp[i] *= j;
            }
        }

        int ans = 0;
        for(int i = 0; i < dp.length; i++) {
            ans += dp[i];
        }
        return ans;
    }
}
```