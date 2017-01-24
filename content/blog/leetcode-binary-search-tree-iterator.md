+++
date = "2017-01-24T22:21:19+08:00"
title = "Binary Search Tree Iterator"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 173"
slug = "leetcode-binary-search-tree-iterator"
+++

### 题目

二叉搜素树迭代器。

Implement an iterator over a binary search tree (BST). Your iterator will be initialized with the root node of a BST.

Calling `next()` will return the next smallest number in the BST.

__Note__: `next()` and `hasNext()` should run in average $O(1)$ time and uses $O(h)$ memory, where $h$ is the height of the tree.

### 分析

思路类似[Binary Tree Inorder Traversal](/blog/leetcode-binary-tree-inorder-traversal)，用一个Stack记录从根节点到当前节点的路径。next的时候就返回Stack最上面的元素。

__注意__：拿出最上面的元素后，还要看一下这个被返回的元素是否有右节点，如果有的话，就把它的右节点及右节点的所有左边节点都压入栈中。另外，初始化栈时，要找到最左边的节点，也就是中序遍历的第一个节点，并把根到第一个节点的路径都压入栈。

### 解法

```java
/**
 * Definition for binary tree
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */

public class BSTIterator {
    Deque<TreeNode> stack;
    
    public BSTIterator(TreeNode root) {
        this.stack = new LinkedList<>();
        while (root != null) {
            stack.push(root);
            root = root.left;
        }
    }

    /** @return whether we have a next smallest number */
    public boolean hasNext() {
        return !stack.isEmpty();
    }

    /** @return the next smallest number */
    public int next() {
        TreeNode cur = stack.pop();
        int ans = cur.val;
        if (cur.right != null) {
            cur = cur.right;
            while (cur != null) {
                stack.push(cur);
                cur = cur.left;
            }
        }
        return ans;
    }
}

/**
 * Your BSTIterator will be called like this:
 * BSTIterator i = new BSTIterator(root);
 * while (i.hasNext()) v[f()] = i.next();
 */
```