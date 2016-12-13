---
title: Integer Break
date: 2016-12-12 18:04:36
categories: 学术
tags: Leetcode
toc: true
mathjax: true
---

Leetcode 343

### 题目

给定一个自然数 n (n ≥ 2），将它拆分成不少于两个自然数之和，对这些拆分后的自然数求积，要求算出最大的乘积。

Given a positive integer n, break it into the sum of at least two positive integers and maximize the product of those integers. Return the maximum product you can get.

For example, given n = 2, return 1 (2 = 1 + 1); given n = 10, return 36 (10 = 3 + 3 + 4).

Note: You may assume that n is not less than 2 and not larger than 58.

__Hint__:

1. There is a simple O(n) solution to this problem.
2. You may check the breaking results of n ranging from 7 to 10 to discover the regularities.


### 分析

发现规律

```
2 = 1 + 1 -> 1
3 = 2 + 1 -> 2
4 = 2 + 2 -> 4
5 = 3 + 2 -> 6
6 = 3 + 3 -> 9
7 = 3 + 2 + 2 -> 12
8 = 3 + 3 + 2 -> 18
9 = 3 + 3 + 3 -> 27
10 = 3 + 3 + 2 + 2 -> 36
```

通项公式：

```
f(2) = 1
f(3) = 2
f(3k) = 3k (k ≥ 2)
f(3k+1) = 2 * 2 * 3k-1 (k ≥ 1)
f(3k+2) = 2 * 3k (k ≥ 1)
```

证明

{% math %}
\begin{aligned}
\frac{\mathrm{d}}{\mathrm{d} x} \left( x^{n/x} \right)\\
= \frac{\mathrm{d}}{\mathrm{d} x} \left( \mathbb{e}^{\frac{n \log{(x)}}{x}} \right)\\
= \left( \frac{\mathrm{d}}{\mathrm{d} x} \left( \frac{n \log{(x)}}{x} \right) \right) \mathbb{e}^\frac{n \log{(x)}}{x}\\
= x^\frac{n}{x} \frac{\mathrm{d}}{\mathrm{d} x} \left( \frac{n \log{(x)}}{x} \right)\\
= n \frac{\mathrm{d}}{\mathrm{d} x} \left( \frac{\log{(x)}}{x} \right) x^{n/x}\\
= \frac{x \frac{\mathrm{d}}{\mathrm{d} x}\left( \log{(x)} \right) - \log{(x)}\frac{\mathrm{d}}{\mathrm{d} x} \left( x \right)}{x^2} n x^{n/x}\\
= nx^{-2 + \frac{n}{x}} \left( -\log{(x)}\left( \frac{\mathrm{d}}{\mathrm{d} x} \left( x \right) \right) + x \left( \frac{\mathrm{d}}{\mathrm{d} x} \left( \log{(x)} \right) \right) \right)\\
= nx^{-2 + \frac{n}{x}} \left( x\left( \frac{\mathrm{d}}{\mathrm{d} x} \left( \log{(x)} \right) \right) - \log{(x)} \right) \\
= nx^{-2 + \frac{n}{x}} \left( -\log{(x)} + \frac{1}{x}x \right) \\
= nx^{-2 + \frac{n}{x}} \left( 1 -\log{(x)} \right)
\end{aligned}
{% endmath %}

其中：

* 第二步，使用[chain rule](https://zh.wikipedia.org/wiki/%E9%93%BE%E5%BC%8F%E6%B3%95%E5%88%99)
* 第五步，使用[quotient rule](https://en.wikipedia.org/wiki/Quotient_rule)

### 解法

```java
public class Solution {
    public int integerBreak(int n) {
        if (n < 3) return 1;
        if (n == 3) return 2;
        int k = n / 3;
        int r = n % 3;
        if (r == 0)
            return (int)Math.pow(3, k);
        else if (r == 1)
            return (int)(4 * Math.pow(3, k - 1));
        else
            return (int)(2 * Math.pow(3, k));
    }
}
```