+++
date = "2016-11-21T16:19:27+08:00"
title = "Repeated Substring Pattern"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 459"
slug = "leetcode-repeated-substring-pattern"
+++

### 题目

判断是否存在重复子串。

Given a non-empty string check if it can be constructed by taking a substring of it and appending multiple copies of the substring together. You may assume the given string consists of lowercase English letters only and its length will not exceed 10000.

__Example 1__:

```console
Input: "abab"

Output: True

Explanation: It's the substring "ab" twice.
```

__Example 2__:

```console
Input: "aba"

Output: False
```

__Example 3__:

```console
Input: "abcabcabcabc"

Output: True

Explanation: It's the substring "abc" four times. (And the substring "abcabc" twice.)
```

### 分析

方法一：暴力解法

时间复杂度 O(k * n)，其中n是字符串长度，k是n的约数个数

若字符串可以由其子串重复若干次构成，则子串的起点一定从原串的下标0开始

并且子串的长度一定是原串长度的约数

整数约数的个数可以通过统计其质因子的幂得到，而输入规模10000以内整数的约数个数很少

因此通过蛮力法，枚举子串长度即可。

### 解法

```java
public class Solution {
    public boolean repeatedSubstringPattern(String str) {
        if (str == null || str.length() == 0) return false;

        int total = str.length();
        int i = 1;
        int k = 0;
        while(i <= total / 2) {
            if(total % i == 0) {
                k = total / i;
                String pattern = str.substring(0, i);
                StringBuilder sb = new StringBuilder();

                for(int j = 0; j < k; j++) {
                    sb.append(pattern);
                }
                if(str.equals(sb.toString())) return true;
            }
            i++;
        }

        return false;
    }
}
```
