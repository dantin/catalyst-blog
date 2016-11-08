---
title: Linked List Cycle
date: 2016-11-07 19:00:54
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 141

### 题目

判断列表中是否有环。

Given a linked list, determine if it has a cycle in it.

__Follow up__:

Can you solve it without using extra space?

### 分析

使用快慢指针，快指针每次走两步；慢指针每次走一步，如果相等则成环。

### 解法

```java
/**
 * Definition for singly-linked list.
 * class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) {
 *         val = x;
 *         next = null;
 *     }
 * }
 */
public class Solution {
    public boolean hasCycle(ListNode head) {
        ListNode fast = head;
        ListNode slow = head;
        do {
            if(fast == null || slow == null) break;
            fast = fast.next;
            if(fast != null) fast = fast.next;
            else break;
            slow = slow.next;
            if(fast == slow) return true;
        } while(fast != slow);
        return false;
    }
}
```