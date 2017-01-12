+++
date = "2016-12-27T16:38:42+08:00"
title = "Combination Sum III"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 216"
slug = "leetcode-combination-sum-iii"
+++

### 题目

寻找所有满足k个数之和等于n的组合，只允许使用数字1-9，并且每一种组合中的数字应该是唯一的。

确保组合中的数字以递增顺序排列。

Find all possible combinations of _k_ numbers that add up to a number _n_, given that only numbers from 1 to 9 can be used and each combination should be a unique set of numbers.


__Example 1__:

```console
Input: k = 3, n = 7

Output:

[[1,2,4]]
```

__Example 2__:

```console
Input: k = 3, n = 9

Output:

[[1,2,6], [1,3,5], [2,3,4]]
```

### 分析

回溯法

### 解法

```java
public class Solution {
    public List<List<Integer>> combinationSum3(int k, int n) {
        List<List<Integer>> ans = new LinkedList<>();
        Deque<Integer> stack = new LinkedList<>();

        dfs(k, n, 1, stack, ans);

        return ans;
    }
    
    private void dfs(int k, int n, int level, Deque<Integer> stack, List<List<Integer>> ans) {
        if (n < 0) return;
        if (n == 0 && stack.size() == k) {
            List<Integer> copy = new LinkedList<>(stack);
            Collections.sort(copy);
            ans.add(copy);
        }
        for (int i = level; i < 10; i++) {
            stack.push(i);
            dfs(k, n - i, i + 1, stack, ans);
            stack.pop();
        }
    }
}
```
