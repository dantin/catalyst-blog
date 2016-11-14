---
title: Pascal's Triangle II
date: 2016-11-11 14:07:54
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 119

### 题目

写出帕斯卡三角第k行的数字，空间复杂度为O(n)。

Given an index k, return the kth row of the Pascal's triangle.

For example, given k = 3,

Return [1,3,3,1].

### 分析

把上面的例子变一下型就清楚了。

```
[
 [1],
 [1,1],
 [1,2,1],
 [1,3,3,1],
 [1,4,6,4,1]
]
```

定义`T[i][j]`为该三角形第i行，第j列的元素，所以可以获得递推函数为

```
   T[i][j] = T[i-1][j] + T[i-1][j-1] if i>0 && j>0
         Or
            =  1  if i=0
         Or
            =  T[i-1][j]  if j=0
```

滚动数组实现。注意Line11，要从后往前加，否则会产生冗余计算。

### 解法

```java
public class Solution {
    public List<Integer> getRow(int rowIndex) {
        List<Integer> row = new ArrayList<>();
        row.add(1);
        for(int i = 1; i <= rowIndex; i++) {
            for(int j = row.size() - 2; j >= 0; j--) {
                row.set(j + 1, row.get(j) + row.get(j+ 1));
            }
            row.add(1);
        }
        return row;
    }
}
```
