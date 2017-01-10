+++
date = "2016-10-26T17:39:34+08:00"
title = "Longest Palindrome"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 409"
slug = "leetcode-longest-palindrome"
+++

### 题目

最长回文。

Given a string which consists of lowercase or uppercase letters, find the length of the longest palindromes that can be built with those letters.

This is case sensitive, for example "Aa" is not considered a palindrome here.

Note:
Assume the length of given string will not exceed 1,010.

__Example__:

```console
Input:
"abccccdd"

Output:
7

Explanation:
One longest palindrome that can be built is "dccaccd", whose length is 7.
```

### 分析

所有的偶数可以用足，所有的奇数可以用n - 1个（除其中的一个奇数可以用全部）。

### 解法

利用全部是大小写字母

```java
public class Solution {
    public int longestPalindrome(String s) {
        int[] charFreqs = new int[26 * 2];
        for(int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if(c >= 'a' && c <= 'z') {
                charFreqs[c - 'a'] += 1;
            }
            if(c >= 'A' && c <= 'Z') {
                charFreqs[c - 'A' + 26] += 1;
            }
        }

        int sum = 0;
        boolean hasOdd = false;
        for(int i = 0; i < charFreqs.length; i++) {
            if(charFreqs[i] % 2 == 0) sum += charFreqs[i];
            else {
                sum += charFreqs[i] - 1;
                hasOdd = true;
            }
        }
        return hasOdd ? sum + 1 : sum;
    }
}
```