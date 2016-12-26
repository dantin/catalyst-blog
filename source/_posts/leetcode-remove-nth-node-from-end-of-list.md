---
title: Remove Nth Node from End of List
date: 2016-11-17 23:58:28
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 19

### 题目

移除链表中倒数第N个元素。

Given a linked list, remove the nth node from the end of list and return its head.

For example,

```
   Given linked list: 1->2->3->4->5, and n = 2.

   After removing the second node from the end, the linked list becomes 1->2->3->5.
```

__Note__:

Given n will always be valid.

Try to do this in one pass.

### 分析

经典题。双指针，一个指针先走n步，然后两个同步走，直到第一个走到终点，第二个指针就是需要删除的节点。唯一要注意的就是头节点的处理，比如：1->2->NULL, n =2; 这时，要删除的就是头节点。

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
    public ListNode removeNthFromEnd(ListNode head, int n) {
        ListNode cur = head;
        ListNode prev = head;
        int step = 0;
        while(step < n && cur != null) {
            cur = cur.next;
            step++;
        }
        if(step == n && cur == null) {
            head = head.next;
            return head;
        }
        while(cur != null && cur.next != null) {
            cur = cur.next;
            prev = prev.next;
        }
        //prev.val = prev.next.val;
        prev.next = prev.next.next;
        return head;
    }
}
```