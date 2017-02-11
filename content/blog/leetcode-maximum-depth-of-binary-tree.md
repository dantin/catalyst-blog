+++
date = "2016-10-20T15:19:23+08:00"
title = "Maximum Depth of Binary Tree"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 104"
slug = "leetcode-maximum-depth-of-binary-tree"
+++

### 题目

求，二叉树深度

Given a binary tree, find its maximum depth.

The maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

### 分析

按层深度遍历，求深度即可。

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
    public int maxDepth(TreeNode root) {
        int depth = 0;
        if (root == null) return depth;
        Queue<TreeNode> queue = new LinkedList<>();
        queue.add(root);
        queue.add(null);
        depth++;

        while (!queue.isEmpty()) {
            TreeNode node = queue.poll();
            if (node == null) {
                if (queue.isEmpty()) {
                    break;
                } else {
                    depth++;
                    queue.add(null);
                }
            } else {
                if (node.left != null) queue.add(node.left);
                if (node.right != null) queue.add(node.right);
            }
        }
        return depth;
    }
}
```
