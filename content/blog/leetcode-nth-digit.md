+++
date = "2016-11-22T18:52:04+08:00"
title = "Nth Digit"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 400"
slug = "leetcode-nth-digit"
+++

### 题目

找出第n个数字。

Find the $n^{th}$ digit of the infinite integer sequence 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ...

__Note__:

n is positive and will fit within the range of a 32-bit signed integer (n < $2^{31}$).

__Example 1__:

```console
Input:
3

Output:
3
```

__Example 2__:

```console
Input:
11

Output:
0

Explanation:
The 11th digit of the sequence 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ... is a 0, which is part of the number 10.
```

### 分析

将整数序列划分为下列区间：

```console
1   1-9
2   10-99
3   100-999
4   1000-9999
5   10000-99999
6   100000-999999
7   1000000-9999999
8   10000000-99999999
9   100000000-99999999
```

然后分区间求值即可，需要注意越界。如：n = 2147483647

### 解法

```java
public class Solution {
    public int findNthDigit(int n) {
        int len = 1;
        long count = 9;
        int start = 1;
        while(n > len * count) {
            n -= (len++) * count;
            count *= 10;
            start *= 10;
        }

        start += (n-1)/len;
        String s = Integer.toString(start);

        return Character.getNumericValue(s.charAt((n-1)%len));
    }
}
```