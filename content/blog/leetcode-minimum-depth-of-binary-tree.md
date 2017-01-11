+++
date = "2016-11-16T17:29:50+08:00"
title = "Minimum Depth of Binary Tree"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 111"
slug = "leetcode-minimum-depth-of-binary-tree"
+++

### 题目

找出二叉树根到任意叶子节点的最短深度。

Given a binary tree, find its minimum depth.

The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.

### 分析

递归，注意只有单一兄弟的情况。

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
    public int minDepth(TreeNode root) {
        if(root == null) return 0;

        int left = minDepth(root.left);
        int right = minDepth(root.right);

        if(left == 0 || right == 0) return Math.max(left, right) + 1;
        return Math.min(left, right) + 1;
    }
}
```
