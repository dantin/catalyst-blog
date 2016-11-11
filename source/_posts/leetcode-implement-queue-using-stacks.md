---
title: Implement Queue using Stacks
date: 2016-11-10 17:38:22
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 232

### 题目

用栈模拟队列。

Implement the following operations of a queue using stacks.

* push(x) -- Push element x to the back of queue.
* pop() -- Removes the element from in front of queue.
* peek() -- Get the front element.
* empty() -- Return whether the queue is empty.

__Notes__:

* You must use only standard operations of a stack -- which means only push to top, peek/pop from top, size, and is empty operations are valid.
* Depending on your language, stack may not be supported natively. You may simulate a stack by using a list or deque (double-ended queue), as long as you use only standard operations of a stack.
* You may assume that all operations are valid (for example, no pop or peek operations will be called on an empty queue).

### 分析

方法一，用一个栈进行模拟。

在执行push操作时，使用辅助栈swap，将栈中元素顺序按照push顺序的逆序存储。

此时，push操作的时间复杂度为O(n)，其余操作的时间复杂度为O(1)。

方法二，用两个栈进行模拟。

维护两个栈inStack与outStack，其中inStack接收push操作新增的元素，outStack为pop/peek操作提供服务

由于栈具有后进先出（Last In First Out）的性质，栈A中的元素依次弹出并压入空栈B之后，栈A中元素的顺序会被逆转

当执行pop或者peek操作时，如果outStack中元素为空，则将inStack中的所有元素弹出并压入outStack，然后对outStack执行相应操作

由于元素至多只会从inStack向outStack移动一次，因此peek/pop操作的平摊开销为O(1)

### 解法

单栈

```java
class MyQueue {
    Stack<Integer> stack = new Stack<>();

    // Push element x to the back of queue.
    public void push(int x) {
        Stack<Integer> temp = new Stack<>();
        while(!stack.empty()) {
            temp.push(stack.pop());
        }
        stack.push(x);
        while(!temp.empty()) {
            stack.push(temp.pop());
        }
    }

    // Removes the element from in front of queue.
    public void pop() {
        stack.pop();
    }

    // Get the front element.
    public int peek() {
        return stack.peek();
    }

    // Return whether the queue is empty.
    public boolean empty() {
        return stack.empty();
    }
}
```

双栈

```java
class MyQueue {
    Stack<Integer> in = new Stack<>();
    Stack<Integer> out = new Stack<>();

    // Push element x to the back of queue.
    public void push(int x) {
        in.push(x);
    }

    // Removes the element from in front of queue.
    public void pop() {
        if(out.empty()) {
            while(!in.empty()) {
                out.push(in.pop());
            }
        }
        out.pop();
    }

    // Get the front element.
    public int peek() {
        if(out.empty()) {
            while(!in.empty()) {
                out.push(in.pop());
            }
        }
        return out.peek();
    }

    // Return whether the queue is empty.
    public boolean empty() {
        return in.empty() && out.empty();
    }
}
```