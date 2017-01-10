+++
date = "2016-11-02T11:29:53+08:00"
title = "Remove Duplicates from Sorted List"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 83"
slug = "leetcode-remove-duplicates-from-sorted-list"
+++

### 题目

从已排序的列表中删除重复项。

Given a sorted linked list, delete all duplicates such that each element appear only once.

For example,

* Given $1 \to 1 \to 2$, return $1 \to 2$.
* Given $1 \to 1 \to 2 \to 3 \to 3$, return $1 \to 2 \to 3$.

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
