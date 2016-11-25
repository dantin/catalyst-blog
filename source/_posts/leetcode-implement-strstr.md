---
title: Implement strStr()
date: 2016-11-24 14:46:23
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 28

### 题目

找出字符串中某子串的下标。

Implement strStr().

Returns the index of the first occurrence of needle in haystack, or -1 if needle is not part of haystack.

### 分析

KMP算法

### 解法

使用JDK原生类。

```java
public class Solution {
    public int strStr(String haystack, String needle) {
        if(haystack == null || needle == null) return -1;
        return haystack.indexOf(needle);
    }
}
```
