---
title: Excel Sheet Column Title
date: 2016-11-28 13:42:01
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 168

### 题目

计算Excel的列头。

Given a positive integer, return its corresponding column title as appear in an Excel sheet.

For example:

```
    1 -> A
    2 -> B
    3 -> C
    ...
    26 -> Z
    27 -> AA
    28 -> AB 
```

### 分析

这道题首先因为26个数字为一组，26次变一次，所以肯定是26进制。

如果是1-26, 那么26号数字没法跟前面保持一致，比如都是一位25/26=0 而26/26=1. 所以应该回归0-based，1-26各数减一变成0-25，对应A到Z。

但新的问题又出现了：AA本来是27，减了一之后是26, 26%26==0，最后一位是A没错，但是前一位26/26 == 1，又对应A，刚才0才对应A来着。所以，__每一循环都要减一__，以确保是0-based

### 解法

```java
public class Solution {
    public String convertToTitle(int n) {
        StringBuilder buf = new StringBuilder();

        while (n > 0) {
            char c = (char)('A' + (n - 1) % 26);
            buf.append(c);
            n = (n - 1) / 26;
        };

        return buf.reverse().toString();
    }
}
```