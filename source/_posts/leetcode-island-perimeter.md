---
title: Island Perimeter
date: 2016-12-18 22:09:15
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 463

### 题目

给定一个二维地图，1表示陆地，0表示水域。单元格水平或者竖直相连（不含对角线）。地图完全被水域环绕，只包含一个岛屿。岛屿没有湖泊。单元格是边长为1的正方形。地图是矩形，长宽不超过100。计算岛屿的周长。

You are given a map in form of a two-dimensional integer grid where 1 represents land and 0 represents water. Grid cells are connected horizontally/vertically (not diagonally). The grid is completely surrounded by water, and there is exactly one island (i.e., one or more connected land cells). The island doesn't have "lakes" (water inside that isn't connected to the water around the island). One cell is a square with side length 1. The grid is rectangular, width and height don't exceed 100. Determine the perimeter of the island.

__Example__:

```
[[0,1,0,0],
 [1,1,1,0],
 [0,1,0,0],
 [1,1,0,0]]

Answer: 16
Explanation: The perimeter is the 16 yellow stripes in the image below:

+-+-+-+-+
|0|1|0|0|
+-+-+-+-+
|1|1|1|0|
+-+-+-+-+
|0|1|0|0|
+-+-+-+-+
|1|1|0|0|
+-+-+-+-+
```

### 分析

每一个陆地单元格的周长为4，当两单元格上下或者左右相邻时，令周长减2。

### 解法

```java
public class Solution {
    public int islandPerimeter(int[][] grid) {
        int sum = 0;
        for (int i = 0; i < grid.length; i++) {
            for (int j = 0; j < grid[i].length; j++) {
                if (grid[i][j] == 1) {
                    sum += 4;
                    if (i > 0 && grid[i - 1][j] == 1) sum -= 2;
                    if (j > 0 && grid[i][j - 1] == 1) sum -= 2;
                }
            }
        }
        return sum;
    }
}
```