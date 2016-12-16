---
title: Integer to Roman
date: 2016-12-16 18:37:38
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 12

### 题目

阿拉伯数字转成罗马数字。

Given an integer, convert it to a roman numeral.

Input is guaranteed to be within the range from 1 to 3999.

### 分析

字母可以重复，但不超过三次，当需要超过三次时，用与下一位的组合表示：

```
I: 1, II: 2, III: 3, IV: 4
C: 100, CC: 200, CCC: 300, CD: 400
```

转化例子：

```
s = 3978
3978/1000 = 3: MMM
978>(1000-100), 998/900 = 1: CM
78<(100-10), 78/50 = 1 :L
28<(50-10), 28/10 = XX
8<(100-1), 8/5 = 1: V
3<(5-1), 3/1 = 3: III
ret = MMMCMLXXVIII
```

### 解法

```java
public class Solution {
    private static final String[] symbol = new String[] {"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"};
    private static final int[] values = new int[] {1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1};

    public String intToRoman(int num) {
        StringBuilder buffer = new StringBuilder();
        int i = 0;
        while(num > 0 && i < symbol.length) {
            while(num >= values[i]) {
                int count = num / values[i];
                num %= values[i];
                for(int j = 0; j < count; j++)
                    buffer.append(symbol[i]);
            }
            i++;
        }
        return buffer.toString();
    }
}
```