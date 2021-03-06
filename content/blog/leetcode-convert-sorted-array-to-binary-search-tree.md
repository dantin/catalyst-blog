+++
date = "2017-01-04T18:58:44+08:00"
title = "Convert Sorted Array to Binary Search Tree"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 108"
slug = "leetcode-convert-sorted-array-to-binary-search-tree"
+++

### 题目

把一个有序数组转化成一棵平衡二叉搜索树。

Given an array where elements are sorted in ascending order, convert it to a height balanced BST.

### 分析

分治法。

自根向下构造BST。
1. 选中间节点为根节点；
2. 左半部分数组元素构造的BST是根节点的左子树；
3. 右半部分数组元素构造的BST是根节点的右子树；
4. 递归；

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
    public TreeNode sortedArrayToBST(int[] nums) {
        return buildTree(nums, 0, nums.length - 1);
    }
    
    private TreeNode buildTree(int[] nums, int start, int end) {
        if (start > end) return null;
        int mid = (start + end) / 2;
        TreeNode node = new TreeNode(nums[mid]);
        node.left = buildTree(nums, start, mid - 1);
        node.right = buildTree(nums, mid + 1, end);
        return node;
    }
}
```