---
title: Balanced Binary Tree
date: 2016-11-10 14:40:08
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 121

### 题目

判断一棵树是否为平衡二叉树。

Given a binary tree, determine if it is height-balanced.

For this problem, a height-balanced binary tree is defined as a binary tree in which the depth of the two subtrees of every node never differ by more than 1.

### 分析

递归：先判断左右子树是不是平衡的，若平衡再求出左右子树的深度，若深度之差大于1，则不平衡。

思路2：在判断左右子树是否平衡的过程中把深度计算出来，这样在对父结点进行平衡判断时就可以不用再重复计算左右子树的深度了。

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
    public boolean isBalanced(TreeNode root) {
        if(root == null) return true;
        if(!isBalanced(root.left)) return false;
        if(!isBalanced(root.right)) return false;

        int left = depth(root.left);
        int right = depth(root.right);
        return Math.abs(left - right) <= 1 ? true : false;
    }
    
    private int depth(TreeNode node) {
        if(node == null) return 0;
        return 1 + Math.max(depth(node.left), depth(node.right));
    }
}
```

因为在遍历每个结点时都要求其左右子树的深度，因此复杂度是`O(n^2)`的。但可以发现，为每个结点计算树的深度是重复的，如左右子树的深度求得的情况下，其直接父亲树的深度就可以不必求了。

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
    public boolean isBalanced(TreeNode root) {
        if(root == null) return true;

        int val = getBalanced(root);
        if(val == -1) return false;
        return true;
    }
    
    private int getBalanced(TreeNode node) {
        if(node == null) return 0;
        int left = getBalanced(node.left);
        if(left == -1) return -1;
        int right = getBalanced(node.right);
        if(right == -1) return -1;
        if(Math.abs(left - right) > 1) return -1;
        return Math.max(left + 1, right + 1);
    }
}
```

相当于后序遍历，因此复杂度是O(n)的。