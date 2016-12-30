---
title: Odd Even Linked List
date: 2016-12-30 11:29:16
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 328

### 题目

求字符串中连续非空子串的数量。

Given a singly linked list, group all odd nodes together followed by the even nodes. Please note here we are talking about the node number and not the value in the nodes.

You should try to do it in place. The program should run in O(1) space complexity and O(nodes) time complexity.

__Example__:

Given `1->2->3->4->5->NULL`
return `1->3->5->2->4->NULL`

__Note__:

The relative order inside both the even and odd groups should remain as it was in the input. 
The first node is considered odd, the second node even and so on ...


### 分析

使用两个指针，odd指向奇节点，even指向偶节点，分别构建奇节点和偶节点的链表，再把偶链表放到奇链表的末尾即可。

如下：

初始状态

```
             +----------+
             | evenHead |
             +----------+
               |
               |
               v
+------+     +----------+     +------+     +---+     +---+     +---+
| even | --> |    2     | --> |  3   | --> | 4 | --> | 5 | --> | ^ |
+------+     +----------+     +------+     +---+     +---+     +---+
               ^
               |
               |
+------+     +----------+     +------+
| odd  | --> |    1     | <-- | head |
+------+     +----------+     +------+
```

合并前状态

```
+----------+     +---+
|   even   | --> | ^ | <----------+
+----------+     +---+            |
                   ^              |
                   |              |
                   |              |
+----------+     +---+            |
|   odd    | --> | 5 | <-----+    |
+----------+     +---+       |    |
                             |    |
                             |    |
                             |    |
+----------+     +---+     +---+  |
|   head   | --> | 1 | --> | 3 |  |
+----------+     +---+     +---+  |
                                  |
                             +----+
                             |
+----------+     +---+     +---+
| evenHead | --> | 2 | --> | 4 |
+----------+     +---+     +---+
```

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
    public ListNode oddEvenList(ListNode head) {
        if (head == null) return head;

        ListNode odd = head, oddHead = head;
        ListNode even = head.next, evenHead = head.next;
        while (even != null && even.next != null) {
            odd.next = even.next;
            odd = odd.next;
            even.next = odd.next;
            even = even.next;
        }
        odd.next = evenHead;

        return oddHead;
    }
}
```