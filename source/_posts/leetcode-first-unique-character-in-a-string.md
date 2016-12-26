---
title: First Unique Character in a String
date: 2016-10-26 17:08:05
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 387

### 题目

判断字符串中第一个唯一字符。

Given a string, find the first non-repeating character in it and return it's index. If it doesn't exist, return -1.

__Examples__:

```
s = "leetcode"
return 0.

s = "loveleetcode",
return 2.
```
__Note__: You may assume the string contain only lowercase letters.

### 分析

构造字符串频率Map，然后线性找到第一个。

### 解法

```java
public class Solution {
    public int firstUniqChar(String s) {
        Map<Character, Long> freqMap = s.chars().mapToObj(i -> (char)i).collect(
            Collectors.groupingBy(c -> c, Collectors.counting()));
        for(int i = 0; i < s.length(); i++) {
            if(freqMap.get(s.charAt(i)) == 1L)
                return i;
        }
        return -1;
    }
}
```

利用全是小写字符的原理

```java
public class Solution {
    public int firstUniqChar(String s) {
        int[] cache = new int[26];
        // 利用Java性质，不用初始化
        // for(char c = 'a'; c <= 'z'; c++)
        //    cache[c - 'a'] = 0;
        for(int i = 0; i < s.length(); i++) {
            cache[s.charAt(i) - 'a'] += 1;
        }

        for(int i = 0; i < s.length(); i++) {
            if(cache[s.charAt(i) - 'a'] == 1)
                return i;
        }
        return -1;
    }
}
```