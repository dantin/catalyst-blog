---
title: Add Two Numbers
date: 2016-04-21 00:03:30
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 2

### 题目

计算两个非负整数列表的和。

You are given two linked lists representing two non-negative numbers. The digits are stored in reverse order and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.

```bash
Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
Output: 7 -> 0 -> 8
```

### 分析

顺序计算每项的和，注意进位需要带入下一次迭代，直至列表遍历完，且不再有进位。时间复杂度O(n)。

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
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode head = null;
        ListNode tail = null;
        int remaining = 0;

        while (l1 != null || l2 != null || remaining != 0) {
            int sum = 0;
            
            if (l1 != null) {
                sum += l1.val;
                l1 = l1.next;
            }
            if (l2 != null) {
                sum += l2.val;
                l2 = l2.next;
            }
            if (remaining != 0) {
                sum += remaining;
            }

            ListNode n = new ListNode(sum % 10);
            if (head == null) {
                head = n;
            }
            if (tail == null) {
                tail = n;
            } else {
                tail.next = n;
                tail = tail.next;
            }
            remaining = sum / 10;
        }

        return head;
    }
}
```
