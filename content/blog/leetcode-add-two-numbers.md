+++
date = "2016-04-21T00:03:30+08:00"
title = "Add Two Numbers"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 2"
slug = "leetcode-add-two-numbers"
+++

### 题目

计算两个非负整数列表的和。

You are given two linked lists representing two non-negative numbers. The digits are stored in reverse order and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.

```console
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
            if (l1 != null) {
                remaining += l1.val;
                l1 = l1.next;
            }
            if (l2 != null) {
                remaining += l2.val;
                l2 = l2.next;
            }

            ListNode n = new ListNode(remaining % 10);
            remaining /= 10;
            if (head == null) {
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
