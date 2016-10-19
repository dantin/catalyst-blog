---
title: Nim Game
date: 2016-10-19 22:00:42
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 292

### 题目

两人一起玩拿棋子的游戏，规则如下：

轮流拿，每次拿的数量是1～3个，最后拿光棋子的人赢得比赛。（备注：两个人都很聪明，都会用最优解法比赛）

给定一个数N，假设A先拿，写一个函数，判断A是否必胜。

You are playing the following Nim Game with your friend: There is a heap of stones on the table, each time one of you take turns to remove 1 to 3 stones. The one who removes the last stone will be the winner. You will take the first turn to remove the stones.

Both of you are very clever and have optimal strategies for the game. Write a function to determine whether you can win the game given the number of stones in the heap.

For example, if there are 4 stones in the heap, then you will never win the game: no matter 1, 2, or 3 stones you remove, the last stone will always be removed by your friend.

### 分析

只有1～3个棋子时，先行拿的人必胜；当有4个棋子时，先拿的人不论如何都会输；把棋子个数放到数轴，每次回朔的步数是1～3步，那么，只要第一次拿完后剩下的棋子是4，则必胜；以此类推...可见`N = 4 * n`时，A必输，以上。

### 解法

```java
public class Solution {
    public boolean canWinNim(int n) {
        return n % 4 != 0;
    }
}
```