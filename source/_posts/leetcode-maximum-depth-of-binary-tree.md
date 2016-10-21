---
title: Maximum Depth of Binary Tree
date: 2016-10-20 15:19:23
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 104

### 题目

求，二叉树深度

Given a binary tree, find its maximum depth.

The maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

### 分析

按层深度遍历，求深度即可。

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
    public int maxDepth(TreeNode root) {
        int depth = 0;
        if(root == null) {
            return depth;
        }
        depth++;
        Queue<Element> queue = new LinkedList<>();
        queue.add(new Element(root, depth));

        while(queue.size() > 0) {
            Element e = queue.poll();
            if(e.level > depth)
                depth = e.level;
            if(e.node.left != null) queue.add(new Element(e.node.left, e.level + 1));
            if(e.node.right != null) queue.add(new Element(e.node.right, e.level + 1));
        }
        return depth;
    }
}

class Element {
    TreeNode node;
    int level;

    Element(TreeNode e, int level) {
        this.node = e;
        this.level = level;
    }
}
```
