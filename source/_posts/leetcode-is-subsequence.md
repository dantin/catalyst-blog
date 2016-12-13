---
title: Is Subsequence
date: 2016-12-13 16:47:01
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 112

### 题目

给定字符串s与字符串t，判断s是否是t的子序列。

Given a string s and a string t, check if s is subsequence of t.

You may assume that there is only lower case English letters in both s and t. t is potentially a very long (length ~= 500,000) string, and s is a short string (<=100).

A subsequence of a string is a new string which is formed from the original string by deleting some (can be none) of the characters without disturbing the relative positions of the remaining characters. (ie, "ace" is a subsequence of "abcde" while "aec" is not).

__Example 1__:

s = "abc", t = "ahbgdc"

Return true.

__Example 2__:

s = "axc", t = "ahbgdc"

Return false.

__Follow up__:

If there are lots of incoming S, say S1, S2, ... , Sk where k >= 1B, and you want to check one by one to see if T has its subsequence. In this scenario, how would you change your code?

### 分析

利用队列（Queue）数据结构。

将s加入队列，遍历t，当t的当前字符c与队头相同时，将队头弹出。

最后判断队列是否为空即可

### 解法

```java
public class Solution {
    public boolean isSubsequence(String s, String t) {
        Queue<Character> queue = new LinkedList<>();
        for(char x : s.toCharArray()) {
            queue.offer(x);
        }

        for(char x : t.toCharArray()) {
            if(!queue.isEmpty() && queue.peek() == x) {
                queue.poll();
            }
        }
        return queue.isEmpty();
    }
}
```

_注意_：`queue.isEmpty()`的判断，否则`peek()`方法可能NPE。