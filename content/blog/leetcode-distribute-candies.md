+++
date = "2017-06-05T22:41:42+08:00"
title = "Distribute Candies"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 575"
slug = "leetcode-distribute-candies"
+++

### 题目

分糖果

Given an integer array with __even__ length, where different numbers in this array represent different __kinds__ of candies. Each number means one candy of the corresponding kind. You need to distribute these candies __equally__ in number to brother and sister. Return the maximum number of __kinds__ of candies the sister could gain.

__Example 1__:

```console
Input: candies = [1,1,2,2,3,3]
Output: 3
Explanation:
There are three different kinds of candies (1, 2 and 3), and two candies for each kind.
Optimal distribution: The sister has candies [1,2,3] and the brother has candies [1,2,3], too. 
The sister has three different kinds of candies. 
```

__Example 2__:

```console
Input: candies = [1,1,2,3]
Output: 2
Explanation: For example, the sister has candies [2,3] and the brother has candies [1,1]. 
The sister has two different kinds of candies, the brother has only one kind of candies. 
```

__Note__:

1. The length of the given array is in range $[2, 10,000]$, and will be even.
2. The number in given array is in range $[-100,000, 100,000]$.

### 分析

利用集合set的自动去重复特性来求出糖的种类数，然后跟n/2比较，取二者之中的较小值返回即可。

### 解法

```go
func distributeCandies(candies []int) int {
    set := make(map[int]bool)
    for _, v := range candies {
        set[v] = true
    }

    if len(set) < len(candies)/2 {
        return len(set)
    }
    return len(candies) / 2
}
```
