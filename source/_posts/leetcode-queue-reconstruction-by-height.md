---
title: Queue Reconstruction by Height
date: 2016-12-04 21:51:29
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 406

### 题目

假设有一队人随机站成一个圈。每个人通过一对整数(h, k)描述，其中h是其身高，k是站在他前面并且身高不低于他的人数。编写算法重构队列。

Suppose you have a random list of people standing in a queue. Each person is described by a pair of integers (h, k), where h is the height of the person and k is the number of people in front of this person who have a height greater than or equal to h. Write an algorithm to reconstruct the queue.

__Note__:

The number of people is less than 1,100.

__Example__

```
Input:
[[7,0], [4,4], [7,1], [5,0], [6,1], [5,2]]

Output:
[[5,0], [7,0], [5,2], [6,1], [4,4], [7,1]]
```

### 分析

首先选出k值为0且身高最低的人，记为hi, ki，将其加入结果集。

然后更新队列，若队列中人员的身高≤hi，则令其k值 - 1（需要记录原始的k值）。

循环直到队列为空。

### 解法

```java
public class Solution {
    public int[][] reconstructQueue(int[][] people) {
        int size = people.length;
        LinkedList<int[]> list = new LinkedList<>();
        for (int i = 0; i < size; i++) {
            list.add(new int[] {people[i][0], people[i][1], 0});
        }
        int[][] ans = new int[size][];
        for (int i = 0; i < size; i++) {
            Collections.sort(list, new Comparator<int[]>() {
                public int compare(int[] a, int[] b) {
                    if (a[1] == b[1]) return a[0] - b[0];
                    return a[1] - b[1];
                }
            });
            int[] head = list.removeFirst();
            ans[i] = new int[] {head[0], head[1] + head[2]};
            for (int[] p : list) {
                if (p[0] <= head[0]) {
                    p[1] -= 1;
                    p[2] += 1;
                }
            }
        }
        return ans;
    }
}
```