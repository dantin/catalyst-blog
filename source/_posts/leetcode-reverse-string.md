---
title: Reverse String
date: 2016-10-19 18:48:51
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 344

### 题目

反转字符串。

Write a function that takes a string as input and returns the string reversed.

Example:

```
Given s = "hello", return "olleh".
```

### 分析

逆序遍历字符串。时间复杂度O(n)。

### 解法

```java
public class Solution {
    public String reverseString(String s) {
        StringBuilder buffer = new StringBuilder();
        for(int i = s.length() - 1; i >= 0; i--) {
            buffer.append(s.charAt(i));
        }

        return buffer.toString();
    }
}
```