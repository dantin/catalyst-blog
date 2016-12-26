---
title: Palindrome Linked List
date: 2016-11-21 10:50:24
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 234

### 题目

判断一个链表是否对称。

Given a singly linked list, determine if it is a palindrome.

__Follow up__:

Could you do it in O(n) time and O(1) space?

### 分析

使用快慢指针寻找链表中点

将链表的后半部分就地逆置，然后比对前后两半的元素是否一致

恢复原始链表的结构

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
    public boolean isPalindrome(ListNode head) {
        if(head == null) return true;

        // find middle
        ListNode fast = head;
        ListNode slow = head;
        while(fast.next != null && fast.next.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }

        // reverse tail part
        ListNode p = slow.next;
        ListNode last = null;
        while(p != null) {
            ListNode next = p.next;
            p.next = last;
            last = p;
            p = next;
        }

        // check palindrome
        ListNode p1 = head;
        ListNode p2 = last;
        while(p2 != null && p1.val == p2.val) {
            p1 = p1.next;
            p2 = p2.next;
        }

        // resume tail part
        p = last;
        last = null;
        while(p != null) {
            ListNode next = p.next;
            p.next = last;
            last = p;
            p = next;
        }
        // re-union list
        slow.next = last;

        return p2 == null;
    }
}
```