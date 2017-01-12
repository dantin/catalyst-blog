+++
date = "2016-12-13T18:22:39+08:00"
title = "Binary Tree Inorder Traversal"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 94"
slug = "leetcode-binary-tree-inorder-traversal"
+++

### 题目

中顺遍历二叉树。

Given a binary tree, return the inorder traversal of its nodes' values.

For example:

Given binary tree $[1,null,2,3]$,

```console
   1
    \
     2
    /
   3
```

return $[1,3,2]$.

__Note__: Recursive solution is trivial, could you do it iteratively?

### 分析

维护一个栈（数据结构）来保存需要但尚未来得及处理的数据。

当遇到一个非空的根结点时，将其压栈，然后递归地（这里用循环来模拟递归）处理其左子结点；当没有左子结点时，从栈中弹出之前遇到的某个根结点（它没有左子结点，或者左子结点已经处理完毕，需要再处理右子结点），打印数据，然后继续处理右子结点。

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
    public List<Integer> inorderTraversal(TreeNode root) {
        Deque<TreeNode> stack = new ArrayDeque<>();

        List<Integer> ans = new LinkedList<>();
        TreeNode cur = root;
        while(cur != null || !stack.isEmpty()) {
            while(cur != null) {
                stack.push(cur);
                cur = cur.left;
            }
            cur = stack.pop();
            ans.add(cur.val);
            cur = cur.right;
        }
        return ans;
    }
}
```