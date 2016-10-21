---
title: Add Digits
date: 2016-10-21 17:27:15
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 258

### 题目

计算任一非负整数的[数根](https://en.wikipedia.org/wiki/Digital_root)。

Given a non-negative integer num, repeatedly add all its digits until the result has only one digit.

For example:

Given num = 38, the process is like: 3 + 8 = 11, 1 + 1 = 2. Since 2 has only one digit, return it.

Follow up:
Could you do it without any loop/recursion in O(1) runtime?

### 分析

顺序计算个数字的和，连进位代入下一轮迭代，直至个位数。

P. S. O(1)的方法还未想到，但是结果Accepted。

### 解法

```java
public class Solution {
    public int addDigits(int num) {
        int sum = 0;
        while (num > 0) {
            sum += num % 10;
            num /= 10;
            if (sum >= 10) {
                num += sum / 10;
                sum %= 10;
            }
        }
        return sum;
    }
}
```
