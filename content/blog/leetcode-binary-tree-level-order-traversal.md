+++
date = "2016-11-07T18:47:30+08:00"
title = "Binary Tree Level Order Traversal"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 102"
slug = "leetcode-binary-tree-level-order-traversal"
+++

### 题目

BFS。

Given a binary tree, return the level order traversal of its nodes' values. (ie, from left to right, level by level).

For example:

Given binary tree $[3,9,20,null,null,15,7]$,

```console
    3
   / \
  9  20
    /  \
   15   7
```

return its level order traversal as:

```console
[
  [3],
  [9,20],
  [15,7]
]
```

### 分析

BFS。

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
    public List<List<Integer>> levelOrder(TreeNode root) {
        Queue<TreeNode> queue = new LinkedList<>();
        if(root != null) queue.add(root);
        List<List<Integer>> res = new LinkedList<>();
        while(queue.size() > 0) {
            LinkedList<TreeNode> sons = new LinkedList<>();
            List<Integer> level = new LinkedList<>();
            while(queue.size() > 0) {
                TreeNode node = queue.poll();
                level.add(node.val);
                if(node.left != null) sons.add(node.left);
                if(node.right != null) sons.add(node.right);
            }
            queue = sons;
            if(level.size() > 0) res.add(level);
        }
        return res;
    }
}
```
