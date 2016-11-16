---
title: Valid Sudoku
date: 2016-11-14 22:57:15
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 36

### 题目

判断数独题目是否合法

Determine if a Sudoku is valid, according to: [Sudoku Puzzles - The Rules](http://sudoku.com.au/TheRules.aspx).

The Sudoku board could be partially filled, where empty cells are filled with the character '.'.

![合理的数独示例](/images/leetcode-valid-sudoku.png "Valid Sudoku")

A partially filled sudoku which is valid.

__Note__:

A valid Sudoku board (partially filled) is not necessarily solvable. Only the filled cells need to be validated.

### 分析

行、列、九宫格分别判断。

### 解法

```java
public class Solution {
    private static final int SIZE = 10;
    
    public boolean isValidSudoku(char[][] board) {
        int[] hash = null;
        for(int i = 0; i < board.length; i++) {
            hash = new int[SIZE];
            for(int j = 0; j < board[i].length; j++) {
                if(board[i][j] >= '1' && board[i][j] <= '9') {
                    hash[board[i][j] - '0']++;
                } else if(board[i][j] == '.') {
                    continue;
                } else {
                    return false;
                }
            }
            if(!isValidGrid(hash)) return false;
        }
        for(int i = 0; i < board.length; i++) {
            hash = new int[SIZE];
            for(int j = 0; j < board[i].length; j++) {
                if(board[j][i] >= '1' && board[j][i] <= '9') {
                    hash[board[j][i] - '0']++;
                } else if(board[j][i] == '.') {
                    continue;
                } else {
                    return false;
                }
            }
            if(!isValidGrid(hash)) return false;
        }
        for(int k = 0; k < 9; k++) {
            hash = new int[SIZE];
            for(int i = k / 3 * 3; i < k / 3 * 3 + 3; i++) {
                for(int j = (k % 3) * 3; j < (k % 3) * 3 + 3; j++) {
                    if(board[i][j] >= '1' && board[i][j] <= '9') {
                        hash[board[i][j] - '0']++;
                    } else if(board[i][j] == '.') {
                        continue;
                    } else {
                        return false;
                    }
                }
            }
            if(!isValidGrid(hash)) return false;
        }
        
        return true;
    }
    
    private boolean isValidGrid(int[] grid) {
        for(int i = 0; i < grid.length; i++) {
            if(grid[i] > 1) return false;
        }
        return true;
    }
}
```