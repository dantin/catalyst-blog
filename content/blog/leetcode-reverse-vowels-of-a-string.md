+++
date = "2016-11-07T14:23:58+08:00"
title = "Reverse Vowels of a String"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 345"
slug = "leetcode-reverse-vowels-of-a-string"
+++

### 题目

反转字符串中的元音字符。

Write a function that takes a string as input and reverse only the vowels of a string.

__Example 1__:

Given s = "hello", return "holle".

__Example 2__:

Given s = "leetcode", return "leotcede".

### 分析

利用StringBuilder和快速排序的思想，互换元音字符，注意边界条件。

### 解法

```java
public class Solution {
    private static final String VOWELS = "aeiouAEIOU";
    
    public String reverseVowels(String s) {
        if(s == null) return "";
        int begin = 0;
        int end = s.length() - 1;
        StringBuilder buf = new StringBuilder(s);
        while(begin < end) {
            while(begin < s.length() && VOWELS.indexOf(buf.charAt(begin)) == -1) begin++;
            while(end >= 0 && VOWELS.indexOf(buf.charAt(end)) == -1) end--;
            if(begin > end) break;
            char t = buf.charAt(begin);
            buf.setCharAt(begin, buf.charAt(end));
            buf.setCharAt(end, t);
            begin++;
            end--;
        }
        return buf.toString();
    }
}
```