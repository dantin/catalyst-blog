+++
date = "2016-10-24T11:32:16+08:00"
title = "Excel Sheet Column Number"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 171"
slug = "leetcode-excel-sheet-column-number"
+++

### 题目

计算Excel的列的对应值。

Related to question Excel Sheet Column Title

Given a column title as appear in an Excel sheet, return its corresponding column number.

For example:

$$
\begin{aligned}
A \to 1\newline
B \to 2\newline
C \to 3\newline
\dots\newline
Z \to 26\newline
AA \to 27\newline
AB \to 28
\end{aligned}
$$

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