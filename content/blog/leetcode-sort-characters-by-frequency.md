+++
date = "2016-12-22T17:04:16+08:00"
title = "Sort Characters By Frequency"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 451"
slug = "leetcode-sort-characters-by-frequency"
+++

### 题目

给定一个字符串，将字符按照出现次数倒序排列。

Given a string, sort it in decreasing order based on the frequency of characters.

__Example 1__:

```console
Input:
"tree"

Output:
"eert"

Explanation:
'e' appears twice while 'r' and 't' both appear once.
So 'e' must appear before both 'r' and 't'. Therefore "eetr" is also a valid answer.
```

__Example 2__:

```console
Input:
"cccaaa"

Output:
"cccaaa"

Explanation:
Both 'c' and 'a' appear three times, so "aaaccc" is also a valid answer.
Note that "cacaca" is incorrect, as the same characters must be together.
```

__Example 3__:

```console
Input:
"Aabb"

Output:
"bbAa"

Explanation:
"bbaA" is also a valid answer, but "Aabb" is incorrect.
Note that 'A' and 'a' are treated as two different characters.
```

### 分析

字符统计 + 排序

### 解法

```java
public class Solution {
    public String frequencySort(String s) {
        int[][] freq = new int[256][2];
        for(char c : s.toCharArray()) {
            freq[c][0] = c;
            freq[c][1]++;
        }

        Arrays.sort(freq, new Comparator<int[]>() {
            @Override
            public int compare(int[] a, int[] b) {
                return b[1] - a[1];
            }
        });

        StringBuilder ans = new StringBuilder();
        for(int i = 0; i < 256; i++) {
            if(freq[i][1] > 0) {
                for(int j = 0; j < freq[i][1]; j++) {
                    ans.append((char)freq[i][0]);
                }
            }
        }

        return ans.toString();
    }
}
```