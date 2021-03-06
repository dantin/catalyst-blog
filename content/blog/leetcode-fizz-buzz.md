+++
date = "2016-10-19T18:33:43+08:00"
title = "Fizz Buzz"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 412"
slug = "leetcode-fizz-buzz"
+++

### 题目

打印特殊序列字符串。

Write a program that outputs the string representation of numbers from 1 to n.

But for multiples of three it should output “Fizz” instead of the number and for the multiples of five output “Buzz”. For numbers which are multiples of both three and five output “FizzBuzz”.

Example:

```console
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

Java:

```java
public class Solution {
    public List<String> fizzBuzz(int n) {
        List<String> list = new LinkedList<>();
        for (int i = 1; i <= n; i++) {
            if (i % 3 == 0 && i % 5 == 0) {
                list.add("FizzBuzz");
            } else if (i % 3 == 0) {
                list.add("Fizz");
            } else if (i % 5 == 0) {
                list.add("Buzz");
            } else {
                list.add(String.valueOf(i));
            }
        }
        return list;
    }
}
```

Golang:

```go
func fizzBuzz(n int) []string {
    r := make([]string, 0)

    for i := 1; i <= n; i++ {
        var s string
        if i % 3 == 0 {
            s = "Fizz"
        }
        if i % 5 == 0 {
            s += "Buzz"
        }
        if len(s) == 0 {
            s = strconv.Itoa(i)
        }

        r = append(r, s)
    }

    return r;
}
```
