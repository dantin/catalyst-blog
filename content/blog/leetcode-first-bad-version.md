+++
date = "2016-11-28T13:38:47+08:00"
title = "First Bad Version"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 278"
slug = "leetcode-first-bad-version"
+++

### 题目

查找第一个错误版本。

You are a product manager and currently leading a team to develop a new product. Unfortunately, the latest version of your product fails the quality check. Since each version is developed based on the previous version, all the versions after a bad version are also bad.

Suppose you have n versions $[1, 2, \dots, n]$ and you want to find out the first bad one, which causes all the following ones to be bad.

You are given an API bool isBadVersion(version) which will return whether version is bad. Implement a function to find the first bad version. You should minimize the number of calls to the API.

### 分析

二分查找，注意溢出条件。

```java
int mid = low + (high - low) / 2;
```

不能简写成

```java
int mid = (high + low) / 2;
```

可能会溢出！！！

### 解法

```java
/* The isBadVersion API is defined in the parent class VersionControl.
      boolean isBadVersion(int version); */

public class Solution extends VersionControl {
    public int firstBadVersion(int n) {
        int low = 1, high = n;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (isBadVersion(mid)) {
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }
        return low;
    }
}
```