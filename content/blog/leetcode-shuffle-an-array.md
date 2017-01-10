+++
date = "2016-12-10T23:22:35+08:00"
title = "Shuffle an Array"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 384"
slug = "leetcode-shuffle-an-array"
+++

### 题目

随机数组中的元素。

Shuffle a set of numbers without duplicates.

__Example__:

```console
// Init an array with set 1, 2, and 3.
int[] nums = {1,2,3};
Solution solution = new Solution(nums);

// Shuffle the array [1,2,3] and return its result. Any permutation of [1,2,3] must equally likely to be returned.
solution.shuffle();

// Resets the array back to its original configuration [1,2,3].
solution.reset();

// Returns the random shuffling of array [1,2,3].
solution.shuffle();
```

### 分析

随机找一个index，然后和数组尾部元素交换，即可。

### 解法

```java
public class Solution {

    private int[] nums;
    private Random random = new Random();
    
    public Solution(int[] nums) {
        this.nums = new int[nums.length];
        System.arraycopy(nums, 0, this.nums, 0, nums.length);    
    }
    
    /** Resets the array to its original configuration and return it. */
    public int[] reset() {
        int[] nums = new int[this.nums.length];
        System.arraycopy(this.nums, 0, nums, 0, this.nums.length);
        return nums;
    }
    
    /** Returns a random shuffling of the array. */
    public int[] shuffle() {
        int[] nums = new int[this.nums.length];
        int length = this.nums.length;
        System.arraycopy(this.nums, 0, nums, 0, length);
        for(int i = 0; i < length; i++) {
            int j = random.nextInt(length - i);
            int tmp = nums[length-1-i];
            nums[length-1-i] = nums[j];
            nums[j] = tmp;
        }
        return nums;
    }
}

/**
 * Your Solution object will be instantiated and called as such:
 * Solution obj = new Solution(nums);
 * int[] param_1 = obj.reset();
 * int[] param_2 = obj.shuffle();
 */
 ```