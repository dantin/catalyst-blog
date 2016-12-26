---
title: Remove Duplicates from Sorted List
date: 2016-11-02 11:29:53
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 83

### 题目

从已排序的列表中删除重复项。

Given a sorted linked list, delete all duplicates such that each element appear only once.

For example,

* Given 1->1->2, return 1->2.
* Given 1->1->2->3->3, return 1->2->3.

### 分析

利用已排序的特点，逐步删除。

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
    public ListNode deleteDuplicates(ListNode head) {
        ListNode h = head;
        while(h != null) {
            if(h.next != null && h.val == h.next.val) {
                h.next = h.next.next;
            } else {
                h = h.next;
            }
        }
        return head;
    }
}
```
