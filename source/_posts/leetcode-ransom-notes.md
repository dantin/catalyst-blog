---
title: Ransom Notes
date: 2016-10-23 22:18:51
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 383

### 题目

赎金字条，判断杂志中的文字是否能够拼凑出字条中的文字。

Given an arbitary ransom note string and another string containing letters from all the magazines, write a function that will return true if the ransom note can be constructed from the magazines; otherwise, it will return false;

Each letter in the magazine string can only be used in your ransom note.

Note:
You may assume that both strings contain only lowercase letters.

```
canConstruct("a", "b") -> false
canConstruct("aa", "ab") -> false
canConstruct("aa", "aab") -> true
```

### 分析

通过杂志中的字符串构造字符频率的Map，再通过赎金字条测试词频是否够用。

### 解法

```java
public class Solution {
    public boolean canConstruct(String ransomNote, String magazine) {
        Map<Character, Integer> ransomMap = new HashMap<>();
        for(int i = 0; i < magazine.length(); i++) {
            Character c = magazine.charAt(i);
            if(!ransomMap.containsKey(c)) {
                ransomMap.put(c, 1);
            } else {
                ransomMap.put(c, ransomMap.get(c) + 1);
            }
        }

        for(int i = 0; i < ransomNote.length(); i++) {
            Character c = ransomNote.charAt(i);
            if(ransomMap.containsKey(c)) {
                int count = ransomMap.get(c);
                if(count > 0) {
                    ransomMap.put(c, count - 1);
                } else {
                    return false;
                }
            } else {
                return false;
            }
        }

        return true;
    }
}
```

Java8特性，因为做了两次词频统计，效率反而慢。

```java
public class Solution {
    public boolean canConstruct(String ransomNote, String magazine) {
        Map<Character, Long> magazineFrequency = magazine.chars().mapToObj(i -> (char)i).collect(
            Collectors.groupingBy(c -> c, Collectors.counting()));
        Map<Character, Long> ransomFrequency = ransomNote.chars().mapToObj(i -> (char)i).collect(
            Collectors.groupingBy(c -> c, Collectors.counting()));
        for(Map.Entry<Character, Long> entry : ransomFrequency.entrySet()) {
            Character key = entry.getKey();
            Long frequency = entry.getValue();

            if(!magazineFrequency.containsKey(key) || magazineFrequency.get(key) < frequency) {
                return false;
            }
        }
        return true;
    }
}
```