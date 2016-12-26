---
title: Valid Anagram
date: 2016-10-26 18:07:18
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 242

### 题目

判断两个字符串是否是Anagram。

所谓Anagram, 就是两个词所用的字母及其个数都是一样的，但是，字母的位置不一样。比如`abcc`和`cbca`就是Anagram中第一个唯一字符。

Given two strings s and t, write a function to determine if t is an anagram of s.

For example,
s = "anagram", t = "nagaram", return true.
s = "rat", t = "car", return false.

Note:
You may assume the string contains only lowercase alphabets.

Follow up:
What if the inputs contain unicode characters? How would you adapt your solution to such case?

### 分析

构造Cache，判断两个字符串的字符频率一致。

### 解法

```java
public class Solution {
    public boolean isAnagram(String s, String t) {
        if(s.length() != t.length()) return false;

        int[] charFreq = new int[26];
        for(int i = 0; i < s.length(); i++) {
            charFreq[s.charAt(i) - 'a'] += 1;
        }
        for(int i = 0; i < t.length(); i++) {
            charFreq[t.charAt(i) - 'a'] -= 1;
        }
        
        for(int x : charFreq) {
            if(x != 0) return false;
        }
        return true;
    }
}
```