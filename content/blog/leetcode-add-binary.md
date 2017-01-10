+++
date = "2016-11-23T18:15:40+08:00"
title = "Add Binary"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 67"
slug = "leetcode-add-binary"
+++


Leetcode 67

### 题目

两个二进制字符串求和。

Given two binary strings, return their sum (also a binary string).

For example,

```
a = "11"
b = "1"
Return "100".
```

### 分析

倒序计算个数字的和，连进位代入下一轮迭代，直至首位。

### 解法

```java
public class Solution {
    public String addBinary(String a, String b) {
        StringBuilder buf = new StringBuilder();
        int sum = 0;
        int ia = a.length();
        int ib = b.length();

        while(ia >0 || ib >0 || sum > 0) {
            int n1 = 0;
            int n2 = 0;

            if(ia > 0) n1 = Character.getNumericValue(a.charAt(--ia));
            if(ib > 0) n2 = Character.getNumericValue(b.charAt(--ib));

            sum += n1 + n2;
            buf.append(sum % 2);
            sum /= 2;
        }
        return buf.reverse().toString();
    }
}
```