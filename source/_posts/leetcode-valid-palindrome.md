---
title: Valid Palindrome
date: 2016-11-28 23:07:18
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 125

### 题目

判断字符串是否是回文。

Given a string, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases.

For example,

"A man, a plan, a canal: Panama" is a palindrome.

"race a car" is not a palindrome.

__Note__:

Have you consider that the string might be empty? This is a good question to ask during an interview.

For the purpose of this problem, we define empty string as valid palindrome.

### 分析

从两头出发，往中间走，进行两两匹配。这里面的小问题就是在这个题目要求中，只判断字母和数字类型的字符，其他字符直接跳过即可。

### 解法

```java
public class Solution {
    public boolean isPalindrome(String s) {
        if (s == null || s.length() == 0) return true;

        char[] str = s.toCharArray();
        int i = 0, j = str.length - 1;
        while (i < j) {
            if (!(Character.isLetter(str[i]) || Character.isDigit(str[i]))) {
                i++;
                continue;
            }
            if (!(Character.isLetter(str[j]) || Character.isDigit(str[j]))) {
                j--;
                continue;
            }
            if (Character.toLowerCase(str[i]) == Character.toLowerCase(str[j])) {
                i++;
                j--;
                continue;
            }
            return false;
        }

        return true;
    }
}
```
