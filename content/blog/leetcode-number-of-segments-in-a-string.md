+++
date = "2016-12-18T23:12:06+08:00"
title = "Number of Segments in a String"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 434"
slug = "leetcode-number-of-segments-in-a-string"
+++


Leetcode 434

### 题目

求字符串中连续非空子串的数量。

Count the number of segments in a string, where a segment is defined to be a contiguous sequence of non-space characters.

Please note that the string does not contain any non-printable characters.

__Example__:

```
Input: "Hello, my name is John"
Output: 5
```

### 分析

遍历字符串，根据状态统计非空子串的个数。

### 解法

```java
public class Solution {
    public int countSegments(String s) {
        if(s == null) return 0;
        int segments = 0;
        boolean in = false;
        for(char c : s.toCharArray()) {
            if(!Character.isSpaceChar(c)) {
                if(!in) segments++;
                in = true;
            } else {
                in = false;
            }
        }
        return segments;
    }
}
```