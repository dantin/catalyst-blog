+++
date = "2016-10-23T22:47:32+08:00"
title = "Delete Node in a Linked List"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 237"
slug = "leetcode-delete-node-in-a-linked-list"
+++

### 题目

删除单链表中的当前节点（当前节点不是尾节点）。

Write a function to delete a node (except the tail) in a singly linked list, given only access to that node.

Supposed the linked list is $1 \to 2 \to 3 \to 4$ and you are given the third node with value $3$, the linked list should become $1 \to 2 \to 4$ after calling your function.

### 分析

因为不知道头节点，所以不能改前置节点的next指向。

注意：因为有个不是尾节点条件，所以可以拷贝下一个节点的值到当前节点，并改变当前节点的next指针指向。


### 解法

```java
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) { val = x; }
 * }
 */
public class Solution {
    public void deleteNode(ListNode node) {
        node.val = node.next.val;
        node.next = node.next.next;
    }
}
```
