+++
date = "2017-01-04T18:29:04+08:00"
title = "Different Ways to Add Parentheses"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 241"
slug = "leetcode-different-ways-to-add-parentheses"
+++


Leetcode 241

### 题目

一个可能含有加减乘的表达式，在任意位置添加括号，求出所有可能表达式的不同值。

Given a string of numbers and operators, return all possible results from computing all the different possible ways to group numbers and operators. The valid operators are `+`, `-` and `*`.

__Example 1__

Input: "`2-1-1`".

```
((2-1)-1) = 0
(2-(1-1)) = 2
```

Output: `[0, 2]`

__Example 2__

Input: "`2*3-4*5`"

```
(2*(3-(4*5))) = -34
((2*3)-(4*5)) = -14
((2*(3-4))*5) = -10
(2*((3-4)*5)) = -10
(((2*3)-4)*5) = 10
```

Output: `[-34, -14, -10, -10, 10]`

### 分析

以2-1-1为例，所有可能的情况：

```
  -           -
 / \         / \
2   -       -   1
   / \     / \
  1   1   2   1
```

得到的结果：2, 0

分治法。

对于输入字符串，若其中有运算符，则将其分为两部分，分别递归计算其值:

* 将左值集合与右值集合进行交叉运算，将运算结果放入结果集中；
* 若没有运算符，则直接将字符串转化为整型数放入结果集中。

### 解法

```java
public class Solution {
    public List<Integer> diffWaysToCompute(String input) {
        List<Integer> ans = new LinkedList<>();
        for (int i = 0; i < input.length(); i++) {
            char ch = input.charAt(i);
            if (ch == '+' || ch == '-' || ch == '*') {
                List<Integer> left = diffWaysToCompute(input.substring(0, i));
                List<Integer> right = diffWaysToCompute(input.substring(i + 1));
                for (int l : left) {
                    for (int r : right) {
                        switch (ch) {
                        case '+':
                            ans.add(l + r);
                            break;
                        case '-':
                            ans.add(l - r);
                            break;
                        case '*':
                            ans.add(l * r);
                            break;
                        }
                    }
                }
            }
        }

        if (ans.size() == 0) {
            ans.add(Integer.parseInt(input));
        }
        return ans;
    }
}
```