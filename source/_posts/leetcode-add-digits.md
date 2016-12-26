---
title: Add Digits
date: 2016-10-21 17:27:15
categories: 练习
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

O(1)解法：

数学归纳法

```
F(n) = n % 9  // if n % 9 != 0
     = 9      // if n % 9 == 0 and n != 0
     = 0      // if n == 0
```

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

O(1)

```java
public class Solution {
    public int addDigits(int num) {
        int digit = num % 9;
        if(num % 9 == 0 && num != 0) {
            digit += 9;
        }
        return digit;
    }
}
```