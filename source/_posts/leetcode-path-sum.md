---
title: Path Sum
date: 2016-11-16 10:41:24
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 112

### 题目

搜索根节点到叶子节点是否存在权制为n的路径。

Given a binary tree and a sum, determine if the tree has a root-to-leaf path such that adding up all the values along the path equals the given sum.

For example:
Given the below binary tree and sum = 22,

```
              5
             / \
            4   8
           /   / \
          11  13  4
         /  \      \
        7    2      1
```

return true, as there exist a root-to-leaf path `5->4->11->2` which sum is 22.

### 分析

递归，二叉树遍历。遍历过程中递减节点值，当到达任意叶节点的时候，进行判断。

### 解法

```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
public class Solution {
    public boolean hasPathSum(TreeNode root, int sum) {
        if(root == null && sum == 0) return false;
        if(root == null) return sum == 0;
        if(sum - root.val == 0 && root.left == null && root.right == null) return true;
        if(root.left != null && hasPathSum(root.left, sum - root.val)) return true;
        if(root.right != null && hasPathSum(root.right, sum - root.val)) return true;

        return false;
    }
}
```
