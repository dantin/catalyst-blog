+++
date = "2017-07-25T08:25:27+08:00"
title = "Merge Two Binary Trees"
categories = ["Code"]
tags = ["Leetcode"]
description = "LeetCode 617"
slug = "leetcode-merge-two-binary-trees"
+++

### 题目

合并两棵树。

Given two binary trees and imagine that when you put one of them to cover the other, some nodes of the two trees are overlapped while the others are not.

You need to merge them into a new binary tree. The merge rule is that if two nodes overlap, then sum node values up as the new value of the merged node. Otherwise, the NOT null node will be used as the node of new tree.

__Example 1__:

```console
Input: 

    Tree 1                     Tree 2   

          1                         2                             
         / \                       / \                            
        3   2                     1   3                        
       /                           \   \                      
      5                             4   7                  

Output: 

Merged tree:

         3
        / \
       4   5
      / \   \ 
     5   4   7
```

### 分析

方法一：递归，依次合并节点。

### 解法

```go
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func mergeTrees(t1 *TreeNode, t2 *TreeNode) *TreeNode {
    if t1 == nil {
        return t2
    }
    if t2 == nil {
        return t1
    }
    t1.Val += t2.Val
    t1.Left = mergeTrees(t1.Left, t2.Left)
    t1.Right = mergeTrees(t1.Right, t2.Right)
    return t1
}
```

解法二：使用栈

```go
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func mergeTrees(t1 *TreeNode, t2 *TreeNode) *TreeNode {
    if t1 == nil {
        return t2
    }

    ss := New()
    ss.Push([]*TreeNode{t1, t2})
    for !ss.IsEmpty() {
        t := ss.Pop().([]*TreeNode)
        if t[0] == nil || t[1] == nil {
            continue
        }
        t[0].Val += t[1].Val
        if t[0].Left == nil {
            t[0].Left = t[1].Left
        } else {
            ss.Push([]*TreeNode{t[0].Left, t[1].Left})
        }
        if t[0].Right == nil {
            t[0].Right = t[1].Right
        } else {
            ss.Push([]*TreeNode{t[0].Right, t[1].Right})
        }
    }
    return t1
}

type Stack struct {
    top    *node
    length int
}

type node struct {
    value interface{}
    prev  *node
}

// Create a new stack
func New() *Stack {
    return &Stack{nil, 0}
}

// Return the number of items in the stack
func (s *Stack) Len() int {
    return s.length
}

// IsEmpty check whether a stack is empty
func (s *Stack) IsEmpty() bool {
    return s != nil && s.length == 0
}

// View the top item on the stack
func (s *Stack) Peek() interface{} {
    if s.length == 0 {
        return nil
    }
    return s.top.value
}

// Pop the top item of the stack and return it
func (s *Stack) Pop() interface{} {
    if s.length == 0 {
        return nil
    }

    n := s.top
    s.top = n.prev
    s.length--
    return n.value
}

// Push a value onto the top of the stack
func (s *Stack) Push(value interface{}) {
    n := &node{value, s.top}
    s.top = n
    s.length++
}
```