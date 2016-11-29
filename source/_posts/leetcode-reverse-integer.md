---
title: Reverse Integer
date: 2016-11-28 22:02:11
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 7

### 题目

反转整数。

Reverse digits of an integer.

__Example1__: x = 123, return 321

__Example2__: x = -123, return -321

### 分析

这道题思路非常简单，就是按照数字位反转过来就可以，基本数字操作。但是这种题的考察重点并不在于问题本身，越是简单的题目越要注意细节，一般来说整数的处理问题要注意的有两点，一点是符号，另一点是整数越界问题。

为后面方便处理，先将数字转为正数。注意Integer.MIN_VALUE的绝对值是比Integer.MAX_VALUE大1的，所以经常要单独处理。如果不先转为正数也可以，只是在后面要对符号进行一下判断。这种题目考察的就是数字的基本处理，面试的时候尽量不能错，而且对于corner case要尽量进行考虑。

### 解法

```java
public class Solution {
    public int reverse(int x) {
        if(x == Integer.MIN_VALUE) return 0;
        
        int num = Math.abs(x);
        int sum = 0;
        while(num != 0) {
            if(sum > (Integer.MAX_VALUE - num % 10)/ 10) return 0;
            sum *= 10;
            sum += num % 10;
            num /= 10;
        }

        return x > 0 ? sum : -sum;
    }
}
```