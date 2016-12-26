---
title: Linked List Random Node
date: 2016-12-07 23:07:36
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 382

### 题目

取链表中的任意节点。

Given a singly linked list, return a random node's value from the linked list. Each node must have the same probability of being chosen.

__Follow up__:

What if the linked list is extremely large and its length is unknown to you? Could you solve this efficiently without using extra space?

Example:

```
// Init a singly linked list [1,2,3].
ListNode head = new ListNode(1);
head.next = new ListNode(2);
head.next.next = new ListNode(3);
Solution solution = new Solution(head);

// getRandom() should return either 1, 2, or 3 randomly. Each element should have equal probability of returning.
solution.getRandom();
```

### 分析

最直接的方法就是先缓存整个链表，然后随机取一个位置。

或者统计出链表的长度，然后根据长度随机生成一个位置，然后从开头遍历到这个位置。

但是，Follow up中说链表可能很长，我们没法提前知道长度，这里用到了著名了[水塘抽样](/2016/12/07/random-sampling-with-a-reservoir/)的思路，由于限定了head一定存在，所以我们先让返回值res等于head的节点值，然后让cur指向head的下一个节点，定义一个变量i，初始化为2，若cur不为空我们开始循环，我们在[0, i - 1]中取一个随机数，如果取出来0，那么我们更新res为当前的cur的节点值，然后此时i自增一，cur指向其下一个位置，这里其实相当于我们维护了一个大小为1的水塘，然后我们随机数生成为0的话，我们交换水塘中的值和当前遍历到底值，这样可以保证每个数字的概率相等

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

    private ListNode head;
    private Random random = new Random();
    /** @param head The linked list's head.
        Note that the head is guaranteed to be not null, so it contains at least one node. */
    public Solution(ListNode head) {
        this.head = head;
    }
    
    /** Returns a random node's value. */
    public int getRandom() {
        int res = head.val;
        int i = 2;
        ListNode cur = head.next;
        while(cur != null) {
            int r = random.nextInt(i);
            if(r == 0) res = cur.val;
            ++i;
            cur = cur.next;
        }
        return res;
    }
}

/**
 * Your Solution object will be instantiated and called as such:
 * Solution obj = new Solution(head);
 * int param_1 = obj.getRandom();
 */
 ```

