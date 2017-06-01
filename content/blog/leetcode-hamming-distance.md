+++
date = "2016-12-19T23:07:33+08:00"
title = "Hamming Distance"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 461"
slug = "leetcode-hamming-distance"
+++

### 题目

求两个数字的[海明距离](https://en.wikipedia.org/wiki/Hamming_distance)。

The [Hamming distance](https://en.wikipedia.org/wiki/Hamming_distance) between two integers is the number of positions at which the corresponding bits are different.

Given two integers x and y, calculate the Hamming distance.

__Note__:

0 ≤ x, y < $2^{31}$.

__Example__:

```console
Input: x = 1, y = 4

Output: 2

Explanation:
1   (0 0 0 1)
4   (0 1 0 0)
       ↑   ↑

The above arrows point to positions where the corresponding bits are different.
```

### 分析

通过异或运算找1的个数。

### 解法

#### Java

```java
public class Solution {
    public int hammingDistance(int x, int y) {
        int d = 0;
        int xor = x ^ y;
        while(xor != 0) {
            d += xor & 1;
            xor /= 2;
        }

        return d;
    }
}
```

#### Python

```python
class Solution(object):
    def hammingDistance(self, x, y):
        """
        :type x: int
        :type y: int
        :rtype: int
        """
        d = 0
        xor = x ^ y
        while xor != 0:
            d += xor & 1;
            xor /= 2;

        return d
```

或使用python原生工具

```python
class Solution(object):
    def hammingDistance(self, x, y):
        """
        :type x: int
        :type y: int
        :rtype: int
        """
        return bin(x^y).count('1')
```

#### Golang

```go
func hammingDistance(x int, y int) int {
    d := 0
    xor := x ^ y
    for xor != 0 {
        d += xor & 1
        xor /= 2
    }
    return d
}
```