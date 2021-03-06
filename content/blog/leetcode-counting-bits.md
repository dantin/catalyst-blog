+++
date = "2016-12-02T11:30:00+08:00"
title = "Counting Bits"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 204"
slug = "leetcode-counting-bits"
+++

### 题目

计算某一范围内个数字二进制中1的个数。

Given a non negative integer number num. For every numbers i in the range 0 ≤ i ≤ num calculate the number of 1's in their binary representation and return them as an array.

__Example__:

For num = 5 you should return $[0,1,1,2,1,2]$.

__Follow up__:

* It is very easy to come up with a solution with run time O(n*sizeof(integer)). But can you do it in linear time O(n) /possibly in a single pass?
* Space complexity should be O(n).
* Can you do it like a boss? Do it without using any builtin function like __builtin_popcount in c++ or in any other language.

__Hint__:

1. You should make use of what you have produced already.
2. Divide the numbers in ranges like $[2-3], [4-7], [8-15]$ and so on. And try to generate new range from previous.
3. Or does the odd/even status of the number help you in calculating the number of 1s?

### 分析

本题采用动规，观察数字的规律：

```console
dp[0] = 0;
dp[1] = dp[0] + 1;
dp[2] = dp[0] + 1;
dp[3] = dp[1] + 1;
dp[4] = dp[0] + 1;
dp[5] = dp[1] + 1;
dp[6] = dp[2] + 1;
dp[7] = dp[3] + 1;
dp[8] = dp[0] + 1;
...
```

类似约瑟夫环的做法

```console
dp[0] = 0;
dp[1] = dp[1-1] + 1;
dp[2] = dp[2-2] + 1;
dp[3] = dp[3-2] + 1;
dp[4] = dp[4-4] + 1;
dp[5] = dp[5-4] + 1;
dp[6] = dp[6-4] + 1;
dp[7] = dp[7-4] + 1;
dp[8] = dp[8-8] + 1;
...
```

得到递推公式：

```console
dp[index] = dp[index - offset] + 1;
```

### 解法

```java
public class Solution {
    public int[] countBits(int num) {
        int[] dp = new int[num + 1];
        int offset = 1;
        for(int i = 1; i <= num; i++) {
            if(i == (offset << 1)) offset <<= 1;
            dp[i] = dp[i-offset] + 1;
        }
        return dp;
    }
}
```