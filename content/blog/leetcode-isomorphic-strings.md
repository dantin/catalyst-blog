+++
date = "2016-11-16T11:12:07+08:00"
title = "Isomorphic Strings"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 112"
slug = "leetcode-isomorphic-strings"
+++


Leetcode 112

### 题目

搜索根节点到叶子节点是否存在权制为n的路径。

Given two strings _s_ and _t_, determine if they are isomorphic.

Two strings are isomorphic if the characters in _s_ can be replaced to get _t_.

All occurrences of a character must be replaced with another character while preserving the order of characters. No two characters may map to the same character but a character may map to itself.

For example,

Given "egg", "add", return true.

Given "foo", "bar", return false.

Given "paper", "title", return true.

Note:
You may assume both s and t have the same length.

### 分析

根据String构造int array，比较int数组进行判断。

### 解法

```java
public class Solution {
    public boolean isIsomorphic(String s, String t) {
        if(s == null && t == null) return true;
        if(s == null || t == null) return false;
        if(s.length() != t.length()) return false;

        int[] is = toIntPattern(s.toCharArray());
        int[] it = toIntPattern(t.toCharArray());

        return Arrays.equals(is, it);
    }
    
    private int[] toIntPattern(char[] s) {
        int code = 0;
        Map<Character, Integer> cp = new HashMap<>();
        int[] pattern = new int[s.length];

        for(int i = 0; i < s.length; i++) {
            char c = s[i];
            if(!cp.containsKey(c)) {
                cp.put(c, code++);
            }
            pattern[i] = cp.get(c);
        }

        return pattern;
    }
}
```
