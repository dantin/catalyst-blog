+++
date = "2017-01-17T09:56:52+08:00"
title = "Random Pick Index"
tags = ["Leetcode"]
description = "Leetcode 398"
slug = "leetcode-random-pick-index"
categories = ["Code"]
+++

### 题目

给定整数数组nums，随机拾取目标数字的标记。

Given an array of integers with possible duplicates, randomly output the index of a given target number. You can assume that the given target number must exist in the array.

__Note__:

The array size can be very large. Solution that uses too much extra space will not pass the judge.

__Example__:

```console
int[] nums = new int[] {1,2,3,3,3};
Solution solution = new Solution(nums);

// pick(3) should return either index 2, 3, or 4 randomly. Each index should have equal probability of returning.
solution.pick(3);

// pick(1) should return 0. Since in the array only nums[0] is equal to 1.
solution.pick(1);
```

### 分析

使用[水塘抽样](/blog/algorithm-random-sampling-with-a-reservoir/)，参考[Linked List Random Node](/blog/leetcode-linked-list-random-node/)

### 解法

```java
public class Solution {

    private int[] nums;
    private Random random;

    public Solution(int[] nums) {
        this.nums = nums;
        this.random = new Random();
    }

    public int pick(int target) {
        int cnt = 0, index = -1;
        for(int i = 0; i < nums.length; i++) {
            if(nums[i] != target) continue;
            cnt++;
            if(random.nextInt(cnt) == 0) index = i;
        }
        return index;
    }
}

/**
 * Your Solution object will be instantiated and called as such:
 * Solution obj = new Solution(nums);
 * int param_1 = obj.pick(target);
 */
```
