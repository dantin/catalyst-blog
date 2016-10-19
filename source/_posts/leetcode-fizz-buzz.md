---
title: Fizz Buzz
date: 2016-10-19 18:33:43
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 412

### 题目

打印特殊序列字符串。

Write a program that outputs the string representation of numbers from 1 to n.

But for multiples of three it should output “Fizz” instead of the number and for the multiples of five output “Buzz”. For numbers which are multiples of both three and five output “FizzBuzz”.

Example:

```bash
n = 15,

Return:
[
    "1",
    "2",
    "Fizz",
    "4",
    "Buzz",
    "Fizz",
    "7",
    "8",
    "Fizz",
    "Buzz",
    "11",
    "Fizz",
    "13",
    "14",
    "FizzBuzz"
]
```

### 分析

顺序打印，注意被3整除、被5整除和被15整除的数字。时间复杂度O(n)。

### 解法

```java
public class Solution {
    public List<String> fizzBuzz(int n) {
        List<String> list = new ArrayList<>();
        for (int i = 1; i <= n; i++) {
            StringBuilder sb = new StringBuilder();
            if (i % 3 == 0) {
                sb.append("Fizz");
            }
            if (i % 5 == 0) {
                sb.append("Buzz");
            }
            if(i % 3 != 0 && i % 5 != 0) {
                sb.append(i);
            }
            list.add(sb.toString());
        }
        return list;
    }
}
```