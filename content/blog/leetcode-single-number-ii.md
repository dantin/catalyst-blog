+++
date = "2016-12-05T23:01:38+08:00"
title = "Single Number II"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 137"
slug = "leetcode-single-number-ii"
+++


Leetcode 137

### 题目

给出 3*n + 1 个的数字，除其中一个数字之外其他每个数字均出现三次，找到这个数字。

Given an array of integers, every element appears three times except for one. Find that single one.

__Note__:

Your algorithm should have a linear runtime complexity. Could you implement it without using extra memory?

### 分析

三个相同的数相加，其二进制位上的每一位也能被3整除。因此只需要一个和int类型相同大小的数组记录每一位累加的结果即可。

### 解法

```java
public class Solution {
    public int singleNumber(int[] nums) {
        int num = 0;
        int[] bits = new int[32];
        for(int i = 0; i < 32; i++) {
            for(int j = 0; j < nums.length; j++) {
                bits[i] += (nums[j] >> i) & 1;
                bits[i] %= 3;
            }
            num |= (bits[i] << i);
        }
        return num;
    }
}
```