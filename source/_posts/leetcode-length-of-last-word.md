---
title: Length of Last Word
date: 2016-11-21 16:41:02
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 58

### 题目

查找字符串中最后一个单词的长度。

Given a string s consists of upper/lower-case alphabets and empty space characters ' ', return the length of last word in the string.

If the last word does not exist, return 0.

__Note__: A word is defined as a character sequence consists of non-space characters only.

For example, 

Given s = "Hello World",
return 5.

### 分析

根据反向扫描字符串，找到第一个Word，计算长度。

注意：字符串尾部包含空格。

### 解法

```java
public class Solution {
    public int lengthOfLastWord(String s) {
        int length = 0;
        if(s == null) return length;
        s = s.trim();
        if(s.length() == 0) return length;

        for(int i = s.length() - 1; i >= 0; i--) {
            char c = s.charAt(i);
            if(c == ' ') break;
            length++;
        }

        return length;
    }
}
```