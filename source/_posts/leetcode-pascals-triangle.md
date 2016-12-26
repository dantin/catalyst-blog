---
title: Pascal's Triangle
date: 2016-11-08 09:55:45
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 118

### 题目

打印杨辉三角（帕斯卡矩阵）。

Given numRows, generate the first numRows of Pascal's triangle.

For example, given numRows = 5,

Return

```
[
     [1],
    [1,1],
   [1,2,1],
  [1,3,3,1],
 [1,4,6,4,1]
]
```

### 分析

头尾都是1，其他元素，满足：

```
a[n] = a[n-1] + a[n]
```

### 解法

```java
public class Solution {
    public List<List<Integer>> generate(int numRows) {
        List<List<Integer>> lines = new LinkedList<>();
        List<Integer> prev = null;
        for(int i = 0; i < numRows; i++) {
            List<Integer> line = new ArrayList<>(i + 1);
            for(int j = 0; j < i + 1; j++) {
                if(j == 0 || j == i) {
                    line.add(1);
                } else {
                    line.add(prev.get(j - 1) + prev.get(j));
                }
            }
            prev = line;
            lines.add(line);
        }
        return lines;
    }
}
```