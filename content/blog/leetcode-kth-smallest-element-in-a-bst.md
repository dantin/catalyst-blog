+++
date = "2016-12-26T15:15:10+08:00"
title = "Kth Smallest Element in a BST"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 230"
slug = "leetcode-kth-smallest-element-in-a-bst"
+++

### 题目

给定一个二叉搜索树，寻找其中的第k小元素。

Given a binary search tree, write a function kthSmallest to find the kth smallest element in it.

__Note__:

You may assume k is always valid, 1 ≤ k ≤ BST's total elements.

__Follow up__:

What if the BST is modified (insert/delete operations) often and you need to find the kth smallest frequently? How would you optimize the kthSmallest routine?

__Hint__:

1. Try to utilize the property of a BST.
2. What if you could modify the BST node's structure?
3. The optimal runtime complexity is O(height of BST).

### 分析

BST的性质最重要的一条就是`左<根<右`，如果用中序遍历所有的节点就会得到一个有序数组。

找到其中第K个元素即可。

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
    public int kthSmallest(TreeNode root, int k) {
        int count = 0;
        Deque<TreeNode> stack = new ArrayDeque<>();
        int target = 0;
        TreeNode cur = root;
        while(cur != null || !stack.isEmpty()) {
            while(cur != null) {
                stack.push(cur);
                cur = cur.left;
            }

            cur = stack.pop();
            count++;
            if(k == count) return cur.val;
            cur = cur.right;
        }
        return 0;
    }
}
```