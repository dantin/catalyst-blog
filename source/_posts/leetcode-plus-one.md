---
title: Plus One
date: 2016-11-07 17:57:30
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 66

### 题目

数组代表的数字加一。

Given a non-negative number represented as an array of digits, plus one to the number.

The digits are stored such that the most significant digit is at the head of the list.

### 分析

直接加，注意进位。

### 解法

```java
public class Solution {
    public int[] plusOne(int[] digits) {
        LinkedList<Integer> list = new LinkedList<>();

        int sum = 1;
        int i = digits.length - 1;
        while(i >= 0) {
            sum += digits[i];
            list.addFirst(sum % 10);
            sum /= 10;
            i--;
        }

        while(sum != 0) {
            list.addFirst(sum % 10);
            sum /= 10;
        }

        int[] res = new int[list.size()];
        i = 0;
        for(Integer n : list) {
            res[i++] = n;
        }

        return res;
    }
}
```