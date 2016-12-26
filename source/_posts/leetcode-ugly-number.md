---
title: Ugly Number
date: 2016-11-02 18:34:20
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 263

### 题目

判断一个数字是否是“丑数”，可以被因式分解2、3、5的幂次积。

Write a program to check whether a given number is an ugly number.

Ugly numbers are positive numbers whose prime factors only include 2, 3, 5. For example, 6, 8 are ugly while 14 is not ugly since it includes another prime factor 7.

Note that 1 is typically treated as an ugly number.

### 分析

分别用2、3、5除输入数字，看看商是否是1。

### 解法

```java
public class Solution {
    public boolean isUgly(int num) {
        if(num <= 0) return false;
        boolean isOps = false;
        while(num != 0) {
            isOps = false;
            if(num % 2 == 0) {num /= 2; isOps = true;}
            if(num % 3 == 0) {num /= 3; isOps = true;}
            if(num % 5 == 0) {num /= 5; isOps = true;}
            if(num == 1) return true;
            if(!isOps) break;
        }
        return false;
    }
}
```