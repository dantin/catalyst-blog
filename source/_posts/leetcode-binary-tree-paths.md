---
title: Binary Tree Paths
date: 2016-11-11 15:11:06
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 257

### 题目

查出二叉树到叶子结点的所有路径。

Given a binary tree, return all root-to-leaf paths.

For example, given the following binary tree:

```
   1
 /   \
2     3
 \
  5
```

All root-to-leaf paths are:

```
["1->2->5", "1->3"]
```

### 分析

DFS，找出左右子节点的所有路径，再加上自己的路径。

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
    public List<String> binaryTreePaths(TreeNode root) {
        List<String> paths = new LinkedList<>();
        if (root == null) return paths;
        
        List<String> left = binaryTreePaths(root.left);
        List<String> right = binaryTreePaths(root.right);
        if (left.size() == 0 && right.size() == 0) {
            paths.add(String.valueOf(root.val));
            return paths;
        } else {
            left.addAll(right);
            for (int i = 0; i < left.size(); i++) {
                StringBuilder buf = new StringBuilder();
                buf.append(root.val);
                buf.append("->");
                buf.append(left.get(i));
                paths.add(buf.toString());
            }
        }

        return paths;
    }
}
```