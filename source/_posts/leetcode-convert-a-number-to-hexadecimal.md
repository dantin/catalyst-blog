---
title: Convert a Number to Hexadecimal
date: 2016-11-01 14:40:54
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 405

### 题目

把一个数字转成它的16进制表示形式。

Given an integer, write an algorithm to convert it to hexadecimal. For negative integer, [two’s complement](https://en.wikipedia.org/wiki/Two%27s_complement) method is used.

__Note__:

1. All letters in hexadecimal (a-f) must be in lowercase.
2. The hexadecimal string must not contain extra leading 0s. If the number is zero, it is represented by a single zero character '0'; otherwise, the first character in the hexadecimal string will not be the zero character.
3. The given number is guaranteed to fit within the range of a 32-bit signed integer.
4. You __must not use any method provided by the library__ which converts/formats the number to hex directly.

__Example 1__:

```
Input:
26

Output:
"1a"
```

__Example 2__:

```
Input:
-1

Output:
"ffffffff"
```

### 分析

每4个bit截取int的二进制数组，直至截取完毕。

### 解法

```java
public class Solution {
    
    final static char[] digits = {
        '0', '1', '2', '3', '4', '5',
        '6', '7', '8', '9', 'a', 'b',
        'c', 'd', 'e', 'f'
    };
    
    public String toHex(int num) {
        StringBuilder buf = new StringBuilder();
        int radix = 1 << 4;
        int mask = radix - 1;
        do {
            buf.append(digits[num & mask]);
            num >>>= 4;
        } while(num != 0);
        
        return buf.reverse().toString();
    }
}
```