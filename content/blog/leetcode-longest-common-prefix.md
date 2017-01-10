+++
date = "2016-11-22T13:55:22+08:00"
title = "Longest Common Prefix"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 14"
slug = "leetcode-longest-common-prefix"
+++


Leetcode 14

### 题目

找字符串的最长前缀。

Write a function to find the longest common prefix string amongst an array of strings.

### 分析

逐个字符比较，时间复杂度为O(N*L)，N是字符串个数，L是最长前缀的长度。

### 解法

```java
public class Solution {
    public String longestCommonPrefix(String[] strs) {
        if(strs == null || strs.length == 0) return "";
        StringBuilder buf = new StringBuilder();
        for(int pos = 0; pos < strs[0].length(); pos++) {
            for(int i = 1; i < strs.length; i++) {
                if(pos >= strs[i].length() || strs[0].charAt(pos) != strs[i].charAt(pos)) {
                    return buf.toString();
                }
            }
            buf.append(strs[0].charAt(pos));
        }

        return buf.toString();
    }
}
```
