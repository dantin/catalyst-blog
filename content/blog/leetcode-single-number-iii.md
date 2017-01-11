+++
date = "2016-12-06T10:03:07+08:00"
title = "Single Number III"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 260"
slug = "leetcode-single-number-iii"
+++

### 题目

数组中有两个数字出现一次，其他数字出现两次，找到这两个数字。

Given an array of numbers nums, in which exactly two elements appear only once and all the other elements appear exactly twice. Find the two elements that appear only once.

For example:

Given nums = $[1, 2, 1, 3, 2, 5]$, return $[3, 5]$.

__Note__:

1. The order of the result is not important. So in the above example, $[5, 3]$ is also correct.
2. Your algorithm should run in linear runtime complexity. Could you implement it using only constant space complexity?

### 分析

对于数组A，假设存在b、c两个数字，在数组中只出现了一次，那么对于整个数组进行异或操作的话，$\oplus[A] = b\oplus c$,  因为其他的数因为出现了两次，异或的过程中就被清零了。

但是仅仅通过最后异或出来的值，是没办法求出b和c的值的，但是足以帮我们把b和c划分到不同的子数组中去。

一个整数有32位bit，对于b和c，除非两者是相同的数，否则一定存在第K位bit，两者是不同的。看下面的例子，

```console
    31 30 29 ... k ... 3 2 1 0
b                1
c                0
b^c          ... 1 ...
```

当找到这个K以后，就可以按照第K位bit是否等于1，将A数组划分成两个子数组，而这两个子数组分别包含了b和c，那么剩下的就只需要把single number的算法直接应用到这两个子数组上，就可以得到b和c了。

### 解法

```java
public class Solution {
    public int[] singleNumber(int[] nums) {
        int xor = 0;
        for(int i = 0; i < nums.length; i++) {
            xor ^= nums[i];
        }

        int mark = 0;
        for(int i = 0; i < 32; i++) {
            if(((xor >> i) & 1) == 1) {
                mark = i;
            }
        }

        int half = 0;
        for(int i = 0; i < nums.length; i++) {
            if(((nums[i] >> mark) & 1) == 1) {
                half ^= nums[i];
            }
        }

        return new int[]{xor ^ half, half};
    }
}
```