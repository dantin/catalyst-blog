---
title: Valid Parentheses
date: 2016-11-18 23:12:14
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 20

### 题目

判断括号字符串是否合法。

Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

The brackets must close in the correct order, "()" and "()[]{}" are all valid but "(]" and "([)]" are not.

### 分析

使用堆栈，每次左括号进来入栈，右括号进来判断合法性，出栈；否则非法。

### 解法

```java
public class Solution {
    private static final Map<Character, Character> parenthes = 
        Collections.unmodifiableMap(new HashMap<Character, Character>() {
        {
            put('(', ')');
            put('[', ']');
            put('{', '}');
        }
    });

    public boolean isValid(String s) {
        Deque<Character> stack = new ArrayDeque<>();

        for (char c : s.toCharArray()) {
            if (parenthes.containsKey(c)) {
                stack.push(c);
            } else {
                Character x = stack.peek();
                if (x != null && c == parenthes.get(x)) {
                    stack.pop();
                } else return false;
            }
        }
        return stack.isEmpty();
    }
}
```

优化一版，其实不需要用Map，能提升性能。

```java
public class Solution {
    public boolean isValid(String s) {
        String left = "([{";
        String right = ")]}";

        Deque<Character> stack = new ArrayDeque<>();
        int pos;

        for (char c : s.toCharArray()) {
            if (left.indexOf(c) != -1) {
                stack.push(c);
            } else {
                Character x = stack.peek();
                if (x != null && (pos = left.indexOf(x)) != -1 && c == right.charAt(pos)) {
                    stack.pop();
                } else return false;
            }
        }
        return stack.isEmpty();
    }
}
```