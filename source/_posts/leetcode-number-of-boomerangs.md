---
title: Number of Boomerangs
date: 2016-11-08 10:50:04
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 447

### 题目

到中心节点距离相同的节点数量。

Given n points in the plane that are all pairwise distinct, a "boomerang" is a tuple of points (i, j, k) such that the distance between i and j equals the distance between i and k (the order of the tuple matters).

Find the number of boomerangs. You may assume that n will be at most 500 and coordinates of points are all in the range \[-10000, 10000\] (inclusive).

__Example__:

```
Input:
[[0,0],[1,0],[2,0]]

Output:
2

Explanation:
The two boomerangs are [[1,0],[0,0],[2,0]] and [[1,0],[2,0],[0,0]]
```

### 分析

枚举点i(x1, y1)，计算点i到各点j(x2, y2)的距离，并分类计数

利用排列组合知识，从每一类距离中挑选2个点的排列数 A(n, 2) = n * (n - 1)

将上述结果累加即为最终答案

### 解法

```java
public class Solution {
    public int numberOfBoomerangs(int[][] points) {
        int sum = 0;
        for(int[] i : points) {
            Map<Integer, Integer> map = new HashMap<>();
            for(int[] j : points) {
                int distance = (i[0] - j[0]) * (i[0] - j[0]) + (i[1] - j[1]) * (i[1] - j[1]);
                if(map.containsKey(distance)) {
                    int count = map.get(distance);
                    map.put(distance, count + 1);
                } else {
                    map.put(distance, 1);
                }
            }
            for(Map.Entry<Integer, Integer> entry : map.entrySet()) {
                int count = entry.getValue();
                sum += count * (count - 1);
            }
        }
        return sum;
    }
}
```
