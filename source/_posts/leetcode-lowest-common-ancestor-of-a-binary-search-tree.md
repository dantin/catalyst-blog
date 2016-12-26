---
title: Lowest Common Ancestor of a Binary Search Tree
date: 2016-11-03 11:51:01
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 235

### 题目

在二叉树中查找两个节点的最近公共父节点。

Given a binary search tree (BST), find the lowest common ancestor (LCA) of two given nodes in the BST.

According to the [definition of LCA on Wikipedia](https://en.wikipedia.org/wiki/Lowest_common_ancestor): “The lowest common ancestor is defined between two nodes v and w as the lowest node in T that has both v and w as descendants (where we allow a node to be a descendant of itself).”

```
        _______6______
       /              \
    ___2__          ___8__
   /      \        /      \
   0      _4       7       9
         /  \
         3   5
```

For example, the lowest common ancestor (LCA) of nodes 2 and 8 is 6. Another example is LCA of nodes 2 and 4 is 2, since a node can be a descendant of itself according to the LCA definition.

### 分析

通过栈搜到根到节点的路径。然后顺序查找最近的公共节点。

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
    private boolean find(TreeNode root, TreeNode target, Deque<TreeNode> stack) {
        if(root == null) return false;
        if(root == target) {
            stack.push(root);
            return true;
        }
        
        if(find(root.left, target, stack)) {stack.push(root); return true;}
        if(find(root.right, target, stack)) {stack.push(root); return true;}
        return false;
    }
    
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        Queue<TreeNode> queue = new LinkedList<>();
        Deque<TreeNode> sp = new ArrayDeque<>();
        Deque<TreeNode> sq = new ArrayDeque<>();
        
        find(root, p, sp);
        find(root, q, sq);

        TreeNode ancestor = null;
        while(sp.size() > 0 && sq.size() > 0) {
            TreeNode ph = sp.pop();
            TreeNode qh = sq.pop();
            if(ph == qh) ancestor = ph;
        }

        return ancestor;
    }
}
```