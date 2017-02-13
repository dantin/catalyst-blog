+++
date = "2016-04-22T22:49:54+08:00"
title = "Longest Substring Without Repeating Characters"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 3"
slug = "leetcode-longest-substring-without-repeating-characters"
+++

### 题目

Given a string, find the length of the longest substring without repeating characters.

__Examples:__

Given "abcabcbb", the answer is "abc", which the length is 3.

Given "bbbbb", the answer is "b", with the length of 1.

Given "pwwkew", the answer is "wke", with the length of 3. Note that the answer must be a substring, "pwke" is a subsequence and not a substring.

### 分析

缓存查询结果，碰到重复字符，重复字符前的子串归位，从重复字符的下一位开始重新找。

### 解法

```java
public class Solution {
    public int lengthOfLongestSubstring(String s) {
        int slow = 0;
        int maxLength = 0;
        int[] hashTable = new int[256];
        for (int i = 0; i < hashTable.length; i++) {
            hashTable[i] = -1;
        }

        for (int fast = 0; fast < s.length(); fast++) {
            int ord = (int)s.charAt(fast);
            if (hashTable[ord] != -1) {
                while (slow <= hashTable[ord]) {
                    hashTable[(int)s.charAt(slow)] = -1;
                    slow++;
                }

            }
            maxLength = Math.max(fast - slow + 1, maxLength);
            hashTable[ord] = fast;
        }
        return maxLength;
    }
}
```
