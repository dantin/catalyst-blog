+++
date = "2016-11-04T14:00:06+08:00"
title = "Binary Tree Level Order Traversal II"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 21"
slug = "leetcode-binary-tree-level-order-traversal-ii"
+++

### 题目

倒序搜索二叉树。

Given a binary tree, return the bottom-up level order traversal of its nodes' values. (ie, from left to right, level by level from leaf to root).

For example:

Given binary tree $[3,9,20,null,null,15,7]$,

```console
    3
   / \
  9  20
    /  \
   15   7
```

return its bottom-up level order traversal as:

```console
[
  [15,7],
  [9,20],
  [3]
]
```

### 分析

BFS放入List，再转置。

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
    public List<List<Integer>> levelOrderBottom(TreeNode root) {
        List<List<Integer>> levels = new LinkedList<>();
        Queue<TreeNode> queue = new LinkedList<>();
        if(root != null) {
            queue.add(root);
        }

        while(queue.size() > 0) {
            Queue<TreeNode> sons = new LinkedList<>();
            List<Integer> level = new ArrayList<>();
            while(queue.size() > 0) {
                TreeNode n = queue.poll();
                level.add(n.val);
                if(n.left != null) sons.add(n.left);
                if(n.right != null) sons.add(n.right);
            }

            if(level.size() > 0) levels.add(level);
            queue = sons;
        }

        Collections.reverse(levels);
        return levels;
    }
}
```