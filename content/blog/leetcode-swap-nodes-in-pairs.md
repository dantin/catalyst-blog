+++
date = "2016-11-07T12:07:37+08:00"
title = "Swap Nodes in Pairs"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 24"
slug = "leetcode-swap-nodes-in-pairs"
+++

### 题目

顺序链表中，每两个一组交换节点位置。

Given a linked list, swap every two adjacent nodes and return its head.

For example,
Given $1 \to 2 \to 3 \to 4$, you should return the list as $2 \to 1 \to 4 \to 3$.

Your algorithm should use only constant space. You may not modify the values in the list, only nodes itself can be changed.

### 分析

顺序扫描，分情况添加后续的两个或一个节点。

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
    public ListNode swapPairs(ListNode head) {
        ListNode current = null;
        ListNode first = null;
        ListNode second = null;
        ListNode tail = null;

        while (head != null) {
            first = head;
            second = first != null ? first.next : first;
            head = second != null ? second.next : first.next;

            if(tail != null) {
                tail.next = (second != null) ? second : first;
            }
            if(second != null) second.next = first;
            tail = first;
            tail.next = null;
            if (current == null) current = (second == null) ? first : second;
        }


        return current;
    }
}
```