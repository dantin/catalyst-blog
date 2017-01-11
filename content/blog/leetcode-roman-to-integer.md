+++
date = "2016-11-02T08:24:08+08:00"
title = "Roman to Integer"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 13"
slug = "leetcode-roman-to-integer"
+++

### 题目

罗马数字表示成阿拉伯数字。

Given a roman numeral, convert it to an integer.

Input is guaranteed to be within the range from 1 to 3999.

### 分析

从后往前扫，递增则加，递减则减。

### 解法

```java
public class Solution {
    private static final Map<Character, Integer> numbers = Collections.unmodifiableMap(new HashMap<Character, Integer>() {
        {
            put('I', 1);
            put('V', 5);
            put('X', 10);
            put('L', 50);
            put('C', 100);
            put('D', 500);
            put('M', 1000);
        }
    });
    
    public int romanToInt(String s) {
        int sum = 0;
        int prev = 0;
        int i = s.length();
        while(i > 0) {
            int n = numbers.get(s.charAt(--i));

            int sig = (n < prev) ? -1 : 1;
            sum += sig * n;
            prev = n;
        }
        
        return sum;
    }
}
```