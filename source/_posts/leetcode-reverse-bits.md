---
title: Reverse Bits
date: 2016-11-24 11:30:17
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 190

### 题目

反转Bit。

Reverse bits of a given 32 bits unsigned integer.

For example, given input 43261596 (represented in binary as 00000010100101000001111010011100), return 964176192 (represented in binary as 00111001011110000010100101000000).

Follow up:
If this function is called many times, how would you optimize it?

### 分析

整型转成bit，补全32位，反转，再解析。

### 解法

```java
public class Solution {
    // you need treat n as an unsigned value
    public int reverseBits(int n) {
        String s = Integer.toBinaryString(n);
        StringBuilder buf = new StringBuilder();
        for(int i = 0; i < 32 - s.length(); i++) {
            buf.append("0");
        }
        buf.append(s);

        return Integer.parseUnsignedInt(buf.reverse().toString(), 2);
    }
}
```

不用自带类优化：

```java
public class Solution {
    // you need treat n as an unsigned value
    public int reverseBits(int n) {
        int res = 0;
        for(int i = 0; i < 32; i++, n >>= 1){
            res = res << 1 | (n & 1);
        }
        return res;
    }
}
```