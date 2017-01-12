+++
date = "2016-10-23T20:38:06+08:00"
title = "Sum of Left Leaves"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 404"
slug = "leetcode-sum-of-left-leaves"
+++

### 题目

求左叶子节点的和。

Find the sum of all left leaves in a given binary tree.

Example:

```console
    3
   / \
  9  20
    /  \
   15   7
```

There are two left leaves in the binary tree, with values 9 and 15 respectively. Return 24.

### 分析

这里需要注意的是左叶子节点，（原本以为是最左叶子节点）因为审题不清楚浪费了很多时间。

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
    public int sumOfLeftLeaves(TreeNode root) {
        int sum = 0;
        int current = 0;
        Queue<TreeNode> queue = new LinkedList<>();
        if (root != null) queue.add(root);
        while (queue.size() > 0) {
            TreeNode node = queue.poll();
            if (node.left != null) queue.add(node.left);
            if (node.right != null) queue.add(node.right);
            if (node.left != null && node.left.left == null && node.left.right == null) {
                sum += node.left.val;
            }
        }
        return sum;
    }
}
```
