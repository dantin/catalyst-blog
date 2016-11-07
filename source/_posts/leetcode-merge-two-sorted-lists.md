---
title: Merge Two Sorted Lists
date: 2016-11-04 11:46:36
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 21

### 题目

合并两个排序的序列。

Merge two sorted linked lists and return it as a new list. The new list should be made by splicing together the nodes of the first two lists.

### 分析

遍历两个列表，按顺序归并。

### 解法

方法一：

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
    public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
        ListNode head = null;
        ListNode tail = null;
        while(l1 != null || l2 != null) {
            ListNode n = null;
            if(l1 != null && l2 != null) {
                if(l1.val <= l2.val) {
                    n = l1;
                    l1 = l1.next;
                } else {
                    n = l2;
                    l2 = l2.next;
                }
            } else if(l1 != null) {
                n = l1;
                l1 = l1.next;
            } else {
                n = l2;
                l2 = l2.next;
            }
            if(head == null) {
                head = n;
                tail = n;
            } else {
                tail.next = n;
                tail = n;
            }
        }
        return head;
    }
}
```

方法二：

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
    public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
        if(l1 == null) return l2;
        if(l2 == null) return l1;
        ListNode head = null;
        ListNode tail = null;

        while(l1 != null && l2 != null) {
            ListNode n = null;
            if(l1.val <= l2.val) {
                n = l1;
                l1 = l1.next;
            } else {
                n = l2;
                l2 = l2.next;
            }
            if(head == null) {
                head = n;
                tail = n;
            } else {
                tail.next = n;
                tail = n;
            }
        }

        if(l1 != null) tail.next = l1;
        if(l2 != null) tail.next = l2;

        return head;
    }
}
```