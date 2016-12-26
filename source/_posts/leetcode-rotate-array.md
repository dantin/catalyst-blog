---
title: Rotate Array
date: 2016-11-29 14:24:07
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 189

### 题目

选择数组。

Rotate an array of n elements to the right by k steps.

For example, with n = 7 and k = 3, the array [1,2,3,4,5,6,7] is rotated to [5,6,7,1,2,3,4].

__Note__:

Try to come up as many solutions as you can, there are at least 3 different ways to solve this problem.

### 分析

直接做超时。

找规律，通过三次反转，我们可以很巧妙的实现旋转数组。首先我们将整个数组反转，然后将前k个数字反转，然后再将后面剩下的数字反转，就得到目标数组了。

```
1, 2, 3, 4, 5, 6, 7
7, 6, 5, 4, 3, 2, 1
5, 6, 7, 4, 3, 2, 1
5, 6, 7, 1, 2, 3, 4
```

注意：

* 反转数组最简单的方法是交换元素，而交换元素有至少三种方法（临时变量，相加相减，异或）
* k可能大于数组长度，旋转不止一次，所以我们要先对k取余

### 解法

直接做法。

```java
public class Solution {
    public void rotate(int[] nums, int k) {
        if (nums == null || nums.length == 0) return;
        for (int j = 0; j < k; j++) {
            int temp = nums[nums.length - 1];
            for (int i = nums.length - 2; i >= 0; i--) {
                nums[i+1] = nums[i];
            }
            nums[0] = temp;
        }
    }
}
```

三次反转

```java
public class Solution {
    public void rotate(int[] nums, int k) {
        k = k % nums.length;
        reverse(nums, 0, nums.length - 1);
        reverse(nums, 0, k - 1);
        reverse(nums, k, nums.length - 1);
    }

    private void reverse(int[] nums, int i, int j) {
        while(i < j) {
            int tmp = nums[i];
            nums[i] = nums[j];
            nums[j] = tmp;
            i++;
            j--;
        }
    }
}
```