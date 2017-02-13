+++
tags = ["Leetcode"]
description = "Leetcode 48"
slug = "leetcode-rotate-image"
date = "2017-02-13T11:38:22+08:00"
title = "Rotate Image"
categories = ["Code"]
+++

### 题目

顺时针90度旋转图像。

You are given an $n \times n$ 2D matrix representing an image.

Rotate the image by 90 degrees (clockwise).

__Follow up__:

Could you do this in-place?

### 分析

直接的方法：

对于当前位置，计算旋转后的新位置，然后再计算下一个新位置，第四个位置又变成当前位置了，所以这个方法每次循环换四个数字，如下所示：

```console
1 2 3       7 2 1       7 4 1
4 5 6  -->  4 5 6  -->  8 5 2　　
7 8 9       9 8 3　 　　 9 6 3
```

首先以从对角线为轴翻转，然后再以x轴中线上下翻转即可得到结果，如下图所示：

```console
1 2 3       9 6 3       7 4 1
4 5 6  -->  8 5 2  -->  8 5 2　　
7 8 9       7 4 1       9 6 3
```

### 解法

方法一：

```java
public class Solution {
    public void rotate(int[][] matrix) {
        int row = matrix.length;
        for (int i = 0; i < row / 2; i++) {
            for (int j = i; j < row - 1 - i; j++) {
                int tmp = matrix[i][j];
                matrix[i][j] = matrix[row - 1 - j][i];
                matrix[row - 1 - j][i] = matrix[row - 1 - i][row - 1 - j];
                matrix[row - 1 - i][row - 1 - j] = matrix[j][row - 1 - i];
                matrix[j][row - 1 - i] = tmp;
            }
        }
    }
}
```

方法二：

```java
public class Solution {
    public void rotate(int[][] matrix) {
        int n = matrix.length;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n - i; j++) {
                int tmp = matrix[i][j];
                matrix[i][j] = matrix[n - 1 - j][n - 1 - i];
                matrix[n - 1 - j][n - 1 - i] = tmp;
            }
        }
        for (int i = 0; i < n / 2; i++) {
            for (int j = 0; j < n; j++) {
                int tmp = matrix[i][j];
                matrix[i][j] = matrix[n - 1 - i][j];
                matrix[n - 1 - i][j] = tmp;
            }
        }
    }
}
```