---
title: Arithmetic Slices
date: 2016-12-04 22:38:38
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 413

### 题目

求数组中等差数列切片的个数。

A sequence of number is called arithmetic if it consists of at least three elements and if the difference between any two consecutive elements is the same.

For example, these are arithmetic sequence:

```
1, 3, 5, 7, 9
7, 7, 7, 7
3, -1, -5, -9
```

The following sequence is not arithmetic.

```
1, 1, 2, 5, 7
```

A zero-indexed array A consisting of N numbers is given. A slice of that array is any pair of integers (P, Q) such that 0 <= P < Q < N.

A slice (P, Q) of array A is called arithmetic if the sequence:

A[P], A[p + 1], ..., A[Q - 1], A[Q] is arithmetic. In particular, this means that P + 1 < Q.

The function should return the number of arithmetic slices in the array A.

__Example__:

```
A = [1, 2, 3, 4]

return: 3, for 3 arithmetic slices in A: [1, 2, 3], [2, 3, 4] and [1, 2, 3, 4] itself.
```

### 分析

若序列S为等差数列，其长度为N，则其等差数列切片的个数

```
SUM = 1 + 2 + ... + (N - 2)
```

### 解法

```java
public class Solution {
    public int numberOfArithmeticSlices(int[] A) {
        if(A == null || A.length < 3) return 0;
        int sum = 0, count = 0;
        int delta = A[1] - A[0];
        for(int i = 2; i < A.length; i++) {
            if(A[i] - A[i-1] == delta) {
                count++;
                sum += count;
            } else {
                delta = A[i] - A[i-1];
                count = 0;
            }
        }
        return sum;
    }
}
```