+++
date = "2016-10-24T19:38:57+08:00"
title = "Same Tree"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 100"
slug = "leetcode-same-tree"
+++

### 题目

判断两个二叉树是否相同。

Given two binary trees, write a function to check if they are equal or not.

Two binary trees are considered equal if they are structurally identical and the nodes have the same value.

### 分析

最简单的办法是递归，判断当前节点和左右子树分别是否相同。

非递归，则使用BFS。

### 解法

递归：

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
    public boolean isSameTree(TreeNode p, TreeNode q) {
        if(p == null && q == null) return true;
        if(p != null && q != null) {
            if(p.val == q.val && isSameTree(p.left, q.left) && isSameTree(p.right, q.right)) {
                return true;
            }
        }
        return false;
    }
}
```

非递归：

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
    public boolean isSameTree(TreeNode p, TreeNode q) {
        Queue<TreeNode> left = new LinkedList<>();
        Queue<TreeNode> right = new LinkedList<>();
        
        left.offer(p);
        right.offer(q);
        while(left.size() > 0 && right.size() > 0) {
            TreeNode ln = left.poll();
            TreeNode rn = right.poll();
            if(ln == null && rn == null) continue;
            if(ln == null || rn == null) return false;
            if(ln.val != rn.val) return false;
            
            left.offer(ln.left);left.offer(ln.right);
            right.offer(rn.left);right.offer(rn.right);
        }
        
        if(left.size() != 0 || right.size() != 0) return false;
        return true;
    }
}
```