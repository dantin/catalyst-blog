+++
date = "2016-11-17T17:54:28+08:00"
title = "Count and Say"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 38"
slug = "leetcode-count-and-say"
+++

### 题目

数数序列。

The count-and-say sequence is the sequence of integers beginning as follows:
1, 11, 21, 1211, 111221, ...

1 is read off as "one 1" or 11.
11 is read off as "two 1s" or 21.
21 is read off as "one 2, then one 1" or 1211.
Given an integer n, generate the nth sequence.

Note: The sequence of integers will be represented as a string.

### 分析

从1开始遍历，直到n，重复则计算计数。

### 解法

```java
public class Solution {
    public String countAndSay(int n) {
        StringBuilder buf = new StringBuilder("1");

        for(int k = 1; k < n; k++) {
            StringBuilder s = new StringBuilder();
            char[] chars = buf.toString().toCharArray();
            char prev = chars[0];
            int count = 1;
            for(int i = 1; i < chars.length; i++) {            
                if(prev == chars[i]) {
                    count++;
                } else {
                    s.append(count);
                    s.append(prev);
                    count = 1;
                    prev = chars[i];
                }
            }
            s.append(count);
            s.append(prev);
            buf = s;
        }
        
        return buf.toString();
    }
}
```