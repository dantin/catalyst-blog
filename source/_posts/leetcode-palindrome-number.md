---
title: Palindrome Number
date: 2016-11-10 17:52:17
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 9

### 题目

判断一个数字是否对称。

Determine whether an integer is a palindrome. Do this without extra space.

### 分析

按位置倒置数字，判断和原数字是否相等。

### 解法

```java
public class Solution {
    public boolean isPalindrome(int x) {
        if(x < 0) {
            return false;
        }

        int value = x;
        int palindrome = 0;

        while(value != 0) {
            palindrome *= 10;
            palindrome += value % 10;
            value /= 10;
        }

        return palindrome == x;
    }
}
```