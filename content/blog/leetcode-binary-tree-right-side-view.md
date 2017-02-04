+++
tags = ["Leetcode"]
description = "Leetcode 199"
slug = "leetcode-binary-tree-right-side-view"
date = "2017-01-26T11:15:33+08:00"
title = "Binary Tree Right Side View"
categories = ["Code"]
+++

### 题目

给定一棵二叉树，返回从右边看这棵二叉树所看到的节点序列（从上到下）。

Given a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can see ordered from top to bottom.

For example:

Given the following binary tree,

```console
   1            <---
 /   \
2     3         <---
 \     \
  5     4       <---
```

You should return $[1, 3, 4]$.

### 分析

层次遍历法。遍历到每层最后一个节点时，把其放到结果集中。

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
    public List<Integer> rightSideView(TreeNode root) {
        List<Integer> ans = new LinkedList<>();
        if (root == null) return ans;

        Queue<TreeNode> queue = new LinkedList<>();
        queue.add(root);
        queue.add(null);

        while (!queue.isEmpty()) {
            TreeNode node = queue.poll();

            if (node == null) {
                if (queue.isEmpty()) {
                    break;
                } else {
                    queue.add(null);
                }
            } else {
                // rightmost node
                if (queue.peek() == null) {
                    ans.add(node.val);
                }

                if (node.left != null) {
                    queue.offer(node.left);
                }
                if (node.right != null) {
                    queue.offer(node.right);
                }
            }
        }

        return ans;
    }
}
```