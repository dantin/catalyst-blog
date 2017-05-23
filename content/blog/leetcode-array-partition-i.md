+++
date = "2017-05-23T12:27:01+08:00"
title = "Array Partition I"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 561"
slug = "leetcode-array-partition-i"
+++

### 题目

数组分组I。

Given an array of $2n$ integers, your task is to group these integers into $n$ pairs of integer, say $(a_1, b_1)$, $(a_2, b_2)$, ..., $(a_n, b_n)$ which makes sum of $min(a_i, b_i)$ for all $i$ from $1$ to $n$ as large as possible.

__Example 1__:

```console
Input: [1,4,3,2]

Output: 4
Explanation: n is 2, and the maximum sum of pairs is 4.
```

Note:

1. n is a positive integer, which is in the range of $[1, 10000]$.
2. All the integers in the array will be in the range of $[-10000, 10000]$.

### 分析

这道题让我们分割数组，两两一对，让每对中较小的数的和最大。

这题用贪婪算法就可以了。由于我们要最大化每对中的较小值之和，那么肯定是每对中两个数字大小越接近越好，因为如果差距过大，而我们只取较小的数字，那么大数字就浪费掉了。明白了这一点，我们只需要给数组排个序，然后按顺序的每两个就是一对，我们取出每对中的第一个数即为较小值累加起来即可。

### 解法

```java
public class Solution {
    public int arrayPairSum(int[] nums) {
        int sum = 0;
        if (nums == null || nums.length == 0) return sum;

        Arrays.sort(nums);
        for (int i = 0; i < nums.length; i++) {
            if (i % 2 == 0) {
                sum += nums[i];
            }
        }
        return sum;
    }
}
```

