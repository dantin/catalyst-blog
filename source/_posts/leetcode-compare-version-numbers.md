---
title: Compare Version Numbers
date: 2016-11-30 22:10:00
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 165

### 题目

比较版本号。

Compare two version numbers version1 and version2.

If version1 > version2 return 1, if version1 < version2 return -1, otherwise return 0.

You may assume that the version strings are non-empty and contain only digits and the `.` character.

The `.` character does not represent a decimal point and is used to separate number sequences.

For instance, 2.5 is not "two and a half" or "half way to version three", it is the fifth second-level revision of the second first-level revision.

Here is an example of version numbers ordering:

```
0.1 < 1.1 < 1.2 < 13.37
```

### 分析

顺序比较每一个部分，但是需要注意一些特殊情况，如：

```
1.0 == 1
```

### 解法

```java
public class Solution {
    public int compareVersion(String version1, String version2) {
        if (version1 == null && version2 == null) return 0;
        if (version1 == null || version1.length() == 0) return -1;
        if (version2 == null || version2.length() == 0) return 1;

        int i1 = 0, i2 = 0;
        while (i1 != version1.length() || i2 != version2.length()) {
            int v1 = 0, v2 = 0;
            if (i1 != version1.length()) {
                int i = version1.indexOf(".", i1);
                v1 = (i == -1) ? Integer.parseInt(version1.substring(i1)) : Integer.parseInt(version1.substring(i1, i));
                i1 = (i == -1) ? version1.length() : i + 1;
            }

            if (i2 != version2.length()) {
                int i = version2.indexOf(".", i2);
                v2 = (i == -1) ? Integer.parseInt(version2.substring(i2)) : Integer.parseInt(version2.substring(i2, i));
                i2 = (i == -1) ? version2.length() : i + 1;
            }

            if (v1 < v2) return -1;
            if (v1 > v2) return 1;
        }

        return 0;
    }
}
```