+++
date = "2016-11-08T09:55:45+08:00"
title = "Pascal's Triangle"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 118"
slug = "leetcode-pascals-triangle"
+++

### 题目

打印杨辉三角（帕斯卡矩阵）。

Given numRows, generate the first numRows of Pascal's triangle.

For example, given numRows = 5,

Return

```console
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

$ a\_n = a\_{n-1} + a\_n $

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