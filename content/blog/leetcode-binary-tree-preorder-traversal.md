+++
date = "2016-12-15T22:42:23+08:00"
title = "Binary Tree Preorder Traversal"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 144"
slug = "leetcode-binary-tree-preorder-traversal"
+++

### 题目

前顺遍历二叉树。

Given a binary tree, return the preorder traversal of its nodes' values.

For example:

Given binary tree {1,#,2,3},

```console
   1
    \
     2
    /
   3
```

return $[1,2,3]$.

__Note__: Recursive solution is trivial, could you do it iteratively?

### 分析

维护一个栈（数据结构）来保存需要但尚未来得及处理的数据。

当遇到一个非空的根结点时，打印数据，再将其压栈，然后递归地（这里用循环来模拟递归）处理其左子结点；当没有左子结点时，从栈中弹出之前遇到的某个根结点（它没有左子结点，或者左子结点已经处理完毕，需要再处理右子结点），然后继续处理右子结点。

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
    public List<Integer> preorderTraversal(TreeNode root) {
        Deque<TreeNode> stack = new ArrayDeque<>();

        List<Integer> ans = new LinkedList<>();
        TreeNode cur = root;
        while(cur != null || !stack.isEmpty()) {
            while(cur != null) {
                ans.add(cur.val);
                stack.push(cur);
                cur = cur.left;
            }

            cur = stack.pop();
            cur = cur.right;
        }

        return ans;
    }
}
```