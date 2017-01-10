+++
date = "2016-12-06T14:58:21+08:00"
title = "Product of Array Except Self"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 238"
slug = "leetcode-product-of-array-except-self"
+++

### 题目

除自身外其他元素的积。

Given an array of n integers where n > 1, nums, return an array output such that $output[i]$ is equal to the product of all the elements of nums except $nums[i]$.

Solve it without division and in O(n).

For example, given $[1,2,3,4]$, return $[24,12,8,6]$.

__Follow up__:

Could you solve it with constant space complexity? (Note: The output array does not count as extra space for the purpose of space complexity analysis.)

### 分析

分解问题：

```console
output[i] =  {i前面的数的乘积}  X  {i后面的数的乘积}
```

问题就解决了，首先从前往后扫描数组一遍，对每一个i，得到{i 前面的数的乘积}(可以称做output_before)，然后在从后往前扫描数组一遍，获得 { i 后面的数的乘积}(可以称做output_after)。将两数相乘即为所求。

举个例子，nums = {1,2,3,4}

第一遍，从前往后扫描一遍，得到的output_before = {1, 1, 2, 6}。

从后往前扫描一遍，得到的output_after = {24, 12, 4, 1}.

则

```console
output[i] = output_before[i] * output_after[i]
output = {24, 12, 8, 6}
```

### 解法

```java
public class Solution {
    public int[] productExceptSelf(int[] nums) {
        int[] output = new int[nums.length];
        long product = 1L;
        for(int i = 0; i < nums.length; i++) {
            output[i] = (int)product;
            product *= nums[i];
        }
        product = 1L;
        for(int i = nums.length - 1; i >=0; i--) {
            output[i] *= (int)product;
            product *= nums[i];
        }

        return output;
    }
}
```