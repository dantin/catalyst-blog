---
title: Excel Sheet Column Number
date: 2016-10-24 11:32:16
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 171

### 题目

计算Excel的列的对应值。

Related to question Excel Sheet Column Title

Given a column title as appear in an Excel sheet, return its corresponding column number.

For example:

```
    A -> 1
    B -> 2
    C -> 3
    ...
    Z -> 26
    AA -> 27
    AB -> 28 
```

### 分析

遍历字符串，每位权重是26，即可

### 解法

```java
public class Solution {
    public int titleToNumber(String s) {
        int sum = 0;
        for(int i = 0; i < s.length(); i++) {
            sum *= 26;
            sum += s.charAt(i) - 'A' + 1;
        }
        return sum;
    }
}
```