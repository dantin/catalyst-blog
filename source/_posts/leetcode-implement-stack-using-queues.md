---
title: Implement Stack using Queues
date: 2016-11-21 11:21:38
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 225

### 题目

用队列模拟堆栈。

Implement the following operations of a stack using queues.

* push(x) -- Push element x onto stack.
* pop() -- Removes the element on top of the stack.
* top() -- Get the top element.
* empty() -- Return whether the stack is empty.

__Notes__:

* You must use only standard operations of a queue -- which means only push to back, peek/pop from front, size, and is empty operations are valid.
* Depending on your language, queue may not be supported natively. You may simulate a queue by using a list or deque (double-ended queue), as long as you use only standard operations of a queue.
* You may assume that all operations are valid (for example, no pop or top operations will be called on an empty stack).

__Update (2015-06-11)__:

The class name of the Java function had been updated to MyStack instead of Stack.

### 分析

方法一，用两个队列模拟。

用两个队列q1，q2实现一个栈。push时把新元素添加到q1的队尾。pop时把q1中除最后一个元素外逐个添加到q2中，然后pop掉q1中的最后一个元素，然后互换q1和q2，以保证我们添加元素时始终向q1中添加。top的道理类似。

push: O(1)，pop: O(n)，top: O(n)

方法二，用两个队列模拟。

所有元素都反序保存在q1中，即后添加的元素在q1的最前端，如何做到呢？每次push时，把新元素放到空的q2，然后把q1中元素逐个添加到q2的队尾，最后交换q1和q2。这样q1队首的元素就是最后添加的元素，pop和top直接返回q1队首的元素就好。

push: O(n)，pop: O(1)，top: O(1)

方法三，一个队列

push时直接添加到队尾就好。pop和top时，把队列除最后一个元素外，逐个循环添加到队列的尾部。

push: O(1)，pop: O(n)，top: O(n)

### 解法

方法一：

```java
class MyStack {
    private Queue<Integer> q1 = new LinkedList<>();
    private Queue<Integer> q2 = new LinkedList<>();

    // Push element x onto stack.
    public void push(int x) {
        q1.offer(x);
    }

    // Removes the element on top of the stack.
    public void pop() {
        while (q1.size() > 1) {
            q2.offer(q1.poll());
        }
        q1.poll();

        Queue<Integer> tmp = q1;
        q1 = q2;
        q2 = tmp;
    }

    // Get the top element.
    public int top() {
        while (q1.size() > 1) {
            q2.offer(q1.poll());
        }
        int top = q1.peek();
        q2.offer(q1.poll());

        Queue<Integer> tmp = q1;
        q1 = q2;
        q2 = tmp;

        return top;
    }

    // Return whether the stack is empty.
    public boolean empty() {
        return q1.isEmpty();
    }
}
```

方法二：

```java
class MyStack {
    private Queue<Integer> q1 = new LinkedList<>();
    private Queue<Integer> q2 = new LinkedList<>();

    // Push element x onto stack.
    public void push(int x) {
        q2.offer(x);
        while(!q1.isEmpty()) {
            q2.offer(q1.poll());
        }

        Queue<Integer> tmp = q1;
        q1 = q2;
        q2 = tmp;
    }

    // Removes the element on top of the stack.
    public void pop() {
        q1.poll();
    }

    // Get the top element.
    public int top() {
        return q1.peek();
    }

    // Return whether the stack is empty.
    public boolean empty() {
        return q1.isEmpty();
    }
}
```

方法三：

```java
class MyStack {
    private Queue<Integer> q = new LinkedList<>();

    // Push element x onto stack.
    public void push(int x) {
        q.offer(x);
    }

    // Removes the element on top of the stack.
    public void pop() {
        int size = q.size();
        for(int i = 1; i < size; i++) {
            q.offer(q.poll());
        }
        q.poll();
    }

    // Get the top element.
    public int top() {
        int size = q.size();
        for(int i = 1; i < size; i++) {
            q.offer(q.poll());
        }
        int top = q.peek();
        q.offer(q.poll());
        return top;
    }

    // Return whether the stack is empty.
    public boolean empty() {
        return q.isEmpty();
    }
}
```