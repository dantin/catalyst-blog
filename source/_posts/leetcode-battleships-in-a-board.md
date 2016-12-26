---
title: Battleships in a Board
date: 2016-12-01 11:12:42
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 419

### 题目

给定一个2维板，计算其中包含多少艘不同的战舰。战舰用字符'X'表示，空白槽位用'.'表示。你应该假设如下规则：

* 给定的板子是有效的，只包含战舰和空白槽位。
* 战舰只能水平或者竖直放置。
* 战舰的尺寸可能不同。
* 两艘战舰之间在水平方向或者竖直方向至少包含一个空间—不会存在相邻的战舰。

Given an 2D board, count how many different battleships are in it. The battleships are represented with 'X's, empty slots are represented with '.'s. You may assume the following rules:

* You receive a valid board, made of only battleships or empty slots.
* Battleships can only be placed horizontally or vertically. In other words, they can only be made of the shape 1xN (1 row, N columns) or Nx1 (N rows, 1 column), where N can be of any size.
* At least one horizontal or vertical cell separates between two battleships - there are no adjacent battleships.

__Example__:

```
X..X
...X
...X
```

In the above board there are 2 battleships.

__Invalid Example__:

```
...X
XXXX
...X
```

This is an invalid board that you will not receive - as battleships will always have a cell separating between them.

__Follow up__:

Could you do it in __one-pass__, using only __O(1) extra memory__ and __without modifying__ the value of the board?

### 分析

由于board中的战舰之间确保有'.'隔开，因此遍历board，若某单元格为'X'，只需判断其左边和上边的相邻单元格是否也是'X'。

如果左邻居或者上邻居单元格是'X'，则说明当前单元格是左边或者上边战舰的一部分；

否则，令计数器+1

### 解法

```java
public class Solution {
    public int countBattleships(char[][] board) {
        int rows = board.length;
        int columns = board[0].length;

        int count = 0;
        for(int row = 0; row < rows; row++) {
            for(int column = 0; column < columns; column++) {
                if(board[row][column] == 'X') {
                    if(row > 0 && board[row - 1][column] == 'X') continue;
                    if(column > 0 && board[row][column - 1] == 'X') continue;
                    count++;
                }
            }
        }
        return count;
    }
}
```

遍历board，用DFS（深度优先搜索）对每一个'X'位置进行探索与标记，同时进行计数。

```python
class Solution(object):
    def countBattleships(self, board):
        """
        :type board: List[List[str]]
        :rtype: int
        """
        vs = set()
        h = len(board)
        w = len(board[0]) if h else 0

        def dfs(x, y):
            for dx, dy in zip((1, 0, -1, 0), (0, 1, 0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < h and 0 <= ny < w:
                    if (nx, ny) not in vs and board[nx][ny] == 'X':
                        vs.add((nx, ny))
                        dfs(nx, ny)

        ans = 0
        for x in range(h):
            for y in range(w):
                if (x, y) not in vs and board[x][y] == 'X':
                    ans += 1
                    vs.add((x, y))
                    dfs(x, y)
        return ans
```
