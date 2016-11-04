---
title: Add Strings
date: 2016-11-01 16:38:07
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 415

### 题目

计算两个字符串的和。

Given two non-negative numbers num1 and num2 represented as string, return the sum of num1 and num2.

__Note__:

1. The length of both num1 and num2 is < 5100.
2. Both num1 and num2 contains only digits 0-9.
3. Both num1 and num2 does not contain any leading zero.
4. You __must not use any built-in BigInteger library__ or __convert the inputs to integer__ directly.

### 分析

依次迭代，注意进位。

### 解法

```java
public class Solution {
    public String addStrings(String num1, String num2) {
        StringBuilder buf = new StringBuilder();
        int sum = 0;
        int radix = 0;
        int i = num1.length();
        int j = num2.length();
        while(i > 0 || j > 0) {
            int a = 0;
            int b = 0;
            if(i > 0) a = num1.charAt(--i) - '0';
            if(j > 0) b = num2.charAt(--j) - '0';
            sum = a + b + radix;
            buf.append(sum % 10);
            radix = sum / 10;
        }

        while(radix > 0) {
            buf.append(radix % 10);
            radix /= 10;
        }

        return buf.reverse().toString();
    }
}
```