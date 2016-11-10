---
title: Word Pattern
date: 2016-11-09 10:45:33
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 290

### 题目

判断字符串是否匹配某一模式。

Given a pattern and a string str, find if str follows the same pattern.

Here __follow__ means a full match, such that there is a bijection between a letter in pattern and a __non-empty__ word in str.

__Examples__:

1. pattern = "abba", str = "dog cat cat dog" should return true.
2. pattern = "abba", str = "dog cat cat fish" should return false.
3. pattern = "aaaa", str = "dog cat cat dog" should return false.
4. pattern = "abba", str = "dog dog dog dog" should return false.

__Notes__:

You may assume pattern contains only lowercase letters, and str contains lowercase letters separated by a single space.

### 分析

阿里笔试题目，要注意模式中的两个不同的字符，不能对应字符串中相同的字符串。

### 解法

方法一：用两个HashMap，字符和字符串需要一一对应。

```java
public class Solution {
    public boolean wordPattern(String pattern, String str) {
        if(pattern == null && str == null) return true;
        if(pattern == null || str == null) return false;
        String[] tokens = str.split("\\s+");
        if(tokens.length != pattern.length()) return false;
        Map<String, Character> smap = new HashMap<>();
        Map<Character, String> cmap = new HashMap<>();
        for(int i = 0; i < tokens.length; i++) {
            String token = tokens[i];
            char c = pattern.charAt(i);
            if(!smap.containsKey(token)) {
                smap.put(token, c);
            }
            if(!cmap.containsKey(c)) {
                cmap.put(c, token);
            }
            if(!cmap.get(c).equals(token) || smap.get(token) != c)
                return false;
        }
        return true;
    }
}
```

方法二：用一个HashMap，但是由于调用了contaisValue()方法，性能会降低。

```java
public class Solution {
    public boolean wordPattern(String pattern, String str) {
        if(pattern == null && str == null) return true;
        if(pattern == null || str == null) return false;
        String[] tokens = str.split("\\s+");
        if(tokens.length != pattern.length()) return false;
        Map<String, Character> map = new HashMap<>();
        for(int i = 0; i < tokens.length; i++) {
            String token = tokens[i];
            char c = pattern.charAt(i);
            if(map.containsKey(token)) {
                if(map.get(token) != c) return false;
            } else if(map.containsValue(c)) {
                return false;
            } else {
                map.put(token, c);
            }
        }
        return true;
    }
}
```

方法三：利用HashMap中put函数的性质。

put函数的声明如下：

```java
public V put(K key, V value)
```

它的功能是将键值对存入map中，如果map中原本就包含要插入的键，将旧值替换为新值。对于该函数的返回值，如果要插入的键在字典中不存在，则返回null，否则返回替换前的值。

利用put()函数的性质和String及Character公共类，Comparable，采用下面的方法：

```java
public class Solution {
    public boolean wordPattern(String pattern, String str) {
        if(pattern == null && str == null) return true;
        if(pattern == null || str == null) return false;
        String[] tokens = str.split("\\s+");
        if(tokens.length != pattern.length()) return false;
        Map<Comparable, Integer> map = new HashMap<>();
        for(int i = 0; i < tokens.length; i++) {
            String token = tokens[i];
            char c = pattern.charAt(i);
            if(!Objects.equals(map.put(c, i), map.put(token, i))) {
                return false;
            }
        }
        return true;
    }
}
```