---
title: Min Stack
date: 2016-11-29 23:11:56
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 155

### 题目

支持最小值的栈。

Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

* push(x) -- Push element x onto stack.
* pop() -- Removes the element on top of the stack.
* top() -- Get the top element.
* getMin() -- Retrieve the minimum element in the stack.

__Example__:

```
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin();   --> Returns -3.
minStack.pop();
minStack.top();      --> Returns 0.
minStack.getMin();   --> Returns -2.
```

### 分析

使用两个栈，一个保存最小值；另一个保存栈值，即可。

优化，一个保存最小值（包括频次）；另一个保存栈值。

### 解法

```java
public class MinStack {

    private Deque<Integer> stack;
    private Deque<Integer> min;

    /** initialize your data structure here. */
    public MinStack() {
        stack = new LinkedList<>();
        min = new LinkedList<>();
    }

    public void push(int x) {
        Integer top = min.peek();
        int num = (top == null) ? x : Math.min(top, x);
        stack.push(x);
        min.push(num);
    }

    public void pop() {
        stack.pop();
        min.pop();
    }

    public int top() {
        return stack.peek();
    }

    public int getMin() {
        return min.peek();
    }
}

/**
 * Your MinStack object will be instantiated and called as such:
 * MinStack obj = new MinStack();
 * obj.push(x);
 * obj.pop();
 * int param_3 = obj.top();
 * int param_4 = obj.getMin();
 */
 ```