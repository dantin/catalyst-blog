---
title: Kth Smallest Element in a Sorted Matrix
date: 2016-12-14 15:07:58
categories: 学术
tags: Leetcode
toc: true
mathjax: true
---

Leetcode 378

### 题目

给定一个`n*n`矩阵，其中每一行每一列都按照递增序排列，寻找矩阵中的第k小元素。

Given a n x n matrix where each of the rows and columns are sorted in ascending order, find the kth smallest element in the matrix.

Note that it is the kth smallest element in the sorted order, not the kth distinct element.

__Example__:

```
matrix = [
   [ 1,  5,  9],
   [10, 11, 13],
   [12, 13, 15]
],
k = 8,

return 13.
```

__Note__:

You may assume k is always valid, $1 \leqslant k \leqslant n^2$.

### 分析

利用最大堆

```
首先将矩阵的左上角（下标0,0）元素加入堆

然后遍历矩阵：

  如果堆大小还未到k，直接入堆；
  反之，如果堆顶元素top大于当前比较元素，入堆；
```

### 解法

```java
public class Solution {
    public int kthSmallest(int[][] matrix, int k) {
        PriorityQueue<Integer> heap = new PriorityQueue<>(
        new Comparator<Integer>() {
            @Override
            public int compare(Integer i0, Integer i1) {
                return i1 - i0;
            }
        });
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[i].length; j++) {
                if (heap.size() < k) {
                    heap.offer(matrix[i][j]);
                } else {
                    if (matrix[i][j] < heap.peek()) {
                        heap.poll();
                        heap.offer(matrix[i][j]);
                    }
                }
            }
        }

        return heap.peek();
    }
}
```