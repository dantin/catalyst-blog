+++
date = "2017-06-01T16:39:09+08:00"
title = "Reshape the matrix"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 566"
slug = "leetcode-reshape-the-matrix"
+++

### 题目

矩阵变形。

In MATLAB, there is a very useful function called 'reshape', which can reshape a matrix into a new one with different size but keep its original data.

You're given a matrix represented by a two-dimensional array, and two __positive__ integers __r__ and __c__ representing the __row__ number and __column__ number of the wanted reshaped matrix, respectively.

The reshaped matrix need to be filled with all the elements of the original matrix in the same __row-traversing__ order as they were.

If the 'reshape' operation with given parameters is possible and legal, output the new reshaped matrix; Otherwise, output the original matrix.

__Example 1__:

```console
Input: 
nums = 
[[1,2],
 [3,4]]
r = 1, c = 4
Output: 
[[1,2,3,4]]
Explanation:
The row-traversing of nums is [1,2,3,4]. The new reshaped matrix is a 1 * 4 matrix, fill it row by row by using the previous list.
```

__Example 2__:

```console
Input: 
nums = 
[[1,2],
 [3,4]]
r = 2, c = 4
Output: 
[[1,2],
 [3,4]]
Explanation:
There is no way to reshape a 2 * 2 matrix to a 2 * 4 matrix. So output the original matrix.
```

__Note__:

1. The height and width of the given matrix is in range $[1, 100]$.
2. The given r and c are all positive.

### 分析

遍历数组，并用老的游标位置更新新的游标位置。

### 解法

```go
func matrixReshape(nums [][]int, r int, c int) [][]int {
    m, n := len(nums), len(nums[0])
    if m * n != r * c {
        return nums
    }

    reshape := make([][]int, r)
    for i := 0; i < r; i++ {
        reshape[i] = make([]int, c)
        for j := 0; j < c; j++ {
            k := i * c + j
            reshape[i][j] = nums[k/n][k%n]
        }
    }

    return reshape
}
```
