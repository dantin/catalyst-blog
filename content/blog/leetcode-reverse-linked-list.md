+++
date = "2016-10-28T15:44:29+08:00"
title = "Reverse Linked List"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 206"
slug = "leetcode-reverse-linked-list"
+++

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