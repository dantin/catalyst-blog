+++
date = "2017-01-05T14:55:17+08:00"
title = "Permutations"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 46"
slug = "leetcode-permutations"
+++


Leetcode 46

### 题目

求数组的全排列。

Given a collection of _distinct_ numbers, return all possible permutations.

For example,

`[1,2,3]` have the following permutations:

```
[
  [1,2,3],
  [1,3,2],
  [2,1,3],
  [2,3,1],
  [3,1,2],
  [3,2,1]
]
```

### 分析

分治法，从前往后进行排列：

* 交换当前节点和选中节点；
* 递归；
* 交换当前节点和选中节点复原；

### 解法

```java
public class Solution {
    public List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> ans = new LinkedList<>();
        permute(nums, 0, ans);
        return ans;
    }

    private void permute(int[] nums, int n, List<List<Integer>> ans) {
        if (n == nums.length) {
            ans.add(Arrays.stream(nums).boxed().collect(Collectors.toList()));
        }
        for (int i = n; i < nums.length; i++) {
            swap(nums, i, n);
            permute(nums, n + 1, ans);
            swap(nums, i, n);
        }
    }

    private void swap(int[] nums, int to, int from) {
        int tmp = nums[from];
        nums[from] = nums[to];
        nums[to] = tmp;
    }
}
```