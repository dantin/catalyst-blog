---
title: Symmetric Tree
date: 2016-11-07 15:15:08
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 101

### 题目

判断两个树是否对称。

Given a binary tree, check whether it is a mirror of itself (ie, symmetric around its center).

For example, this binary tree [1,2,2,3,4,4,3] is symmetric:

```
    1
   / \
  2   2
 / \ / \
3  4 4  3
```

But the following [1,2,2,null,3,null,3] is not:

```
    1
   / \
  2   2
   \   \
   3    3
```

### 分析

递归方法，只需要判断当前节点、子节点、孙子节点，并从孙子节点递归判断即可。

非递归方法，分层判断。

### 解法

递归

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
    public boolean isSymmetric(TreeNode root) {
        if(root == null) return true;
        return isSymmetric(root.left, root.right);
    }
    
    private boolean isSymmetric(TreeNode left, TreeNode right) {
        if(left == null) return right == null;
        if(right == null) return left == null;
        if(left.val != right.val) return false;
        if(!isSymmetric(left.left, right.right)) return false;
        if(!isSymmetric(left.right, right.left)) return false;
        return true;
    }
}
```

非递归

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
    public boolean isSymmetric(TreeNode root) {
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        while(queue.size() > 0) {
            LinkedList<TreeNode> sons = new LinkedList<>();
            while(queue.size() > 0) {
                TreeNode node = queue.poll();
                if(node == null) continue;
                sons.add(node.left);
                sons.add(node.right);
            }

            int i = 0;
            int j = sons.size() - 1;

            while(i < j && i < sons.size() && j >= 0) {
                if(
                    (sons.get(i) == null && sons.get(j) == null) || 
                    (sons.get(i) != null && sons.get(j) != null && sons.get(i).val == sons.get(j).val)) {
                    i++;
                    j--;
                } else {
                    return false;
                }
            }
            queue = sons;
        }
        return true;
    }
}
```