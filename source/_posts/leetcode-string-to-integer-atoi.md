---
title: String to Integer(atoi)
date: 2016-11-30 22:52:56
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 8

### 题目

字符串转数字，实现atoi函数。

Implement atoi to convert a string to an integer.

__Hint__: Carefully consider all possible input cases. If you want a challenge, please do not see below and ask yourself what are the possible input cases.

__Notes__: It is intended for this problem to be specified vaguely (ie, no given input specs). You are responsible to gather all the input requirements up front.

### 分析

逐次计算，注意边界条件。

另外，用long型存放最终结果。

### 解法

```java
public class Solution {
    public int myAtoi(String str) {
        if (str == null || str.length() == 0) return 0;
        int i = 0;
        while (i < str.length() && Character.isWhitespace(str.charAt(i))) i++;

        boolean flag = false;
        long sum = 0;
        if (str.charAt(i) == '-') {
            flag = true;
            i++;
        } else if (str.charAt(i) == '+') {
            flag = false;
            i++;
        } else if (!Character.isDigit(str.charAt(i)))
            return 0;

        while (i < str.length() && Character.isDigit(str.charAt(i))) {
            sum *= 10;
            sum += str.charAt(i++) - '0';
            if (sum > Integer.MAX_VALUE) break;
            if (sum < Integer.MIN_VALUE) break;
        }

        sum = flag ? -1 * sum : sum;

        if (sum > Integer.MAX_VALUE) return Integer.MAX_VALUE;
        if (sum < Integer.MIN_VALUE) return Integer.MIN_VALUE;
        return (int)sum;
    }
}
```