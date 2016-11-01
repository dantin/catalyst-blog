---
title: Reverse Linked List
date: 2016-10-28 15:44:29
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 206

### 题目

反转链表。

Reverse a singly linked list.

### 分析

遍历，反转。

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
    public ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode current = head;
        while(current != null) {
             head = current;
             current = current.next;
             head.next = prev;
             prev = head;
        }
        return head;
    }
}
```