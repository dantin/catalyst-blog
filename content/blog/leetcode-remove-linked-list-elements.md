+++
date = "2016-11-21T17:08:27+08:00"
title = "Remove Linked List Elements"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 203"
slug = "leetcode-remove-linked-list-elements"
+++


Leetcode 203

### 题目

移除链表中值为特定目标的所有节点。

Remove all elements from a linked list of integers that have value val.

Example

```
Given: 1 --> 2 --> 6 --> 3 --> 4 --> 5 --> 6, val = 6
Return: 1 --> 2 --> 3 --> 4 --> 5
```

### 分析

遍历链表，如果节点的值等于目标，跳过；反之，加入结果链表。

注意：头、中、尾节点。

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
    public ListNode removeElements(ListNode head, int val) {
        ListNode h = null;
        ListNode tail = null;

        while(head != null) {

            if(head.val == val) {
                head = head.next;
                continue;
            }

            if(tail == null) {
                h = head;
                tail = h;
            } else {
                tail.next = head;
                tail = tail.next;
            }
            head = head.next;
        }
        if(tail != null && tail.next != null) tail.next = null;

        return h;
    }
}
```
