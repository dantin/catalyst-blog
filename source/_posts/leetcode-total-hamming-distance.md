---
title: Total Hamming Distance
date: 2016-12-27 09:52:05
categories: 练习
tags: Leetcode
toc: true
mathjax: true
---

Leetcode 477

### 题目

求两个整数之间的[海明距离](https://en.wikipedia.org/wiki/Hamming_distance)。

The [Hamming distance](https://en.wikipedia.org/wiki/Hamming_distance) between two integers is the number of positions at which the corresponding bits are different.

Now your job is to find the total Hamming distance between all pairs of the given numbers.

__Example__:

```
Input: 4, 14, 2

Output: 6

Explanation: In binary representation, the 4 is 0100, 14 is 1110, 
and 2 is 0010 (just showing the four bits relevant in this case). 

So the answer will be:
HammingDistance(4, 14) + HammingDistance(4, 2) + HammingDistance(14, 2)
 = 2 + 2 + 2 = 6.
```

__Note__:

1. Elements of the given array are in the range of 0 to $10^9$
2. Length of the array will not exceed $10^4$.

### 分析

按位统计各整数的二进制位置i上的0与1的个数之和，分别记为zero, 和one，其中：`zero + one = len(num)`

{% math %}
\begin{aligned}
\sum_{i=0}^{31} C_{zero}^1 C_{one}^{1}
\end{aligned}
{% endmath %}

### 解法

暴力解法

```java
public class Solution {
    public int totalHammingDistance(int[] nums) {
        int ans = 0;
        for (int i = 0; i < nums.length; i++) {
            for (int j = 0; j < i; j++) {
                ans += Integer.bitCount(nums[i] ^ nums[j]);
            }
        }
        return ans;
    }
}
```

优化解法

```java
public class Solution {
    public int totalHammingDistance(int[] nums) {
        int ans = 0;

        for (int i = 0; i < 32; i++) {
            int zero = 0, one = 0;
            int mask = 1 << i;
            for (int n : nums) {
                if ((mask & n) == 0) {
                    zero++;
                } else {
                    one++;
                }
            }
            ans += one * zero;
        }
        return ans;
    }
}
```
