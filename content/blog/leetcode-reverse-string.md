+++
date = "2016-10-19T18:48:51+08:00"
title = "Reverse String"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 344"
slug = "leetcode-reverse-string"
+++


Leetcode 344

### 题目

反转字符串。

Write a function that takes a string as input and returns the string reversed.

Example:

```console
Given s = "hello", return "olleh".
```

### 分析

逆序遍历字符串。时间复杂度O(n)。

交换前后指针。时间复杂度O(n)。

### 解法

方法一：

```java
public class Solution {
    public String reverseString(String s) {
        StringBuilder buffer = new StringBuilder();
        for(int i = s.length() - 1; i >= 0; i--) {
            buffer.append(s.charAt(i));
        }

        return buffer.toString();
    }
}
```

方法二：

```java
public class Solution {
    public String reverseString(String s) {
        char[] buffer = s.toCharArray();
        int i = 0, j = buffer.length - 1;
        while (i < j) {
            char tmp = buffer[i];
            buffer[i++] = buffer[j];
            buffer[j--] = tmp;
        }

        return new String(buffer);
    }
}
```

方法三：

```java
public class Solution {
    public String reverseString(String s) {
        StringBuilder buffer = new StringBuilder(s);
        return buffer.reverse().toString();
    }
}
```