---
title: Invert Binary Tree
date: 2016-10-21 18:02:21
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 226

### 题目

反转二叉树。

Invert a binary tree.

```
     4
   /   \
  2     7
 / \   / \
1   3 6   9
```

to

```
     4
   /   \
  7     2
 / \   / \
9   6 3   1
```

This problem was inspired by [this original tweet](https://twitter.com/mxcl/status/608682016205344768) by [Max Howell](https://twitter.com/mxcl):

> Google: 90% of our engineers use the software you wrote (Homebrew), but you can’t invert a binary tree on a whiteboard so fuck off.

### 分析

广度优先搜索即可。

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
    public TreeNode invertTree(TreeNode root) {
        Queue<TreeNode> queue = new LinkedList<>();
        if(root != null) queue.add(root);
        while(queue.size() > 0) {
            TreeNode n = queue.poll();
            if(n.left != null) queue.add(n.left);
            if(n.right != null) queue.add(n.right);
            TreeNode t = n.left;
            n.left = n.right;
            n.right = t;
        }
        return root;
    }
}
```
