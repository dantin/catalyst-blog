---
title: Happy Number
date: 2016-11-02 10:56:21
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 202

### 题目

判断Happy Number。

Write an algorithm to determine if a number is "happy".

A happy number is a number defined by the following process: Starting with any positive integer, replace the number by the sum of the squares of its digits, and repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1. Those numbers for which this process ends in 1 are happy numbers.

__Example__: 19 is a happy number

```
1^2 + 9^2 = 82
8^2 + 2^2 = 68
6^2 + 8^2 = 100
1^2 + 0^2 + 0^2 = 1
```

### 分析

拆分分别判断，因为可能存在循环，所以用一个set保存中间结果。

### 解法

```java
public class Solution {
    public boolean isHappy(int n) {
        int sum = 0;
        int num = n;
        Set<Integer> set = new HashSet<>();

        while(true) {
            sum = 0;
            while(num > 0) {
                sum += (num % 10) * (num % 10);
                num /= 10;
            }
            num = sum;
            if(set.contains(num)) break;
            set.add(num);
            if(num == 1) return true;
        }
        return false;
    }
}
```