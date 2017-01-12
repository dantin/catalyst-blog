+++
date = "2016-12-28T22:10:37+08:00"
title = "4sum II"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 454"
slug = "leetcode-4sum-ii"

+++

### 题目

在四个数组中各取一个数字，使其和为0。

Given four lists A, B, C, D of integer values, compute how many tuples $(i, j, k, l)$ there are such that $A[i] + B[j] + C[k] + D[l]$ is zero.

To make problem a bit easier, all A, B, C, D have same length of N where 0 ≤ N ≤ 500. All integers are in the range of $-2^{28}$ to $2^{28} - 1$ and the result is guaranteed to be at most $2^{31} - 1$.

__Example__:

```console
Input:
A = [ 1, 2]
B = [-2,-1]
C = [-1, 2]
D = [ 0, 2]

Output:
2

Explanation:
The two tuples are:
1. (0, 0, 0, 1) -> A[0] + B[0] + C[0] + D[1] = 1 + (-2) + (-1) + 2 = 0
2. (1, 1, 0, 0) -> A[1] + B[1] + C[0] + D[0] = 2 + (-1) + (-1) + 0 = 0
```

### 分析

最普通的方法就是遍历所有的情况，时间复杂度为O($n^4$)。

如果把A和B的两两之和都求出来，在哈希表中建立两数之和跟其出现次数之间的映射，那么我们再遍历C和D中任意两个数之和，我们只要看哈希表存不存在这两数之和的相反数，可以把时间复杂度提升到O($n^2$)。

### 解法

```java
public class Solution {
    public int fourSumCount(int[] A, int[] B, int[] C, int[] D) {
        Map<Integer, Integer> cache = new HashMap<>();
        int ans = 0;
        int key;
        for (int i = 0; i < A.length; i++) {
            for (int j = 0; j < B.length; j++) {
                key = A[i] + B[j];
                if (cache.containsKey(key)) {
                    cache.put(key, cache.get(key) + 1);
                } else {
                    cache.put(key, 1);
                }
            }
        }

        for (int i = 0; i < C.length; i++) {
            for (int j = 0; j < D.length; j++) {
                key = -1 * (C[i] + D[j]);
                ans += cache.getOrDefault(key, 0);
            }
        }
        return ans;
    }
}
```