---
title: Generate Parentheses
date: 2016-12-30 16:26:42
categories: 练习
tags: Leetcode
toc: true
mathjax: true
---

Leetcode 22

### 题目

所有合理的括号排列。

Given $n$ pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

For example, given $n = 3$, a solution set is:

```
[
  "((()))",
  "(()())",
  "(())()",
  "()(())",
  "()()()"
]
```

### 分析

可以使用[卡特兰数](/2016/12/30/math-catalan-number/)的性质。

递归思想。

给定的n为括号对，所以就是有n个左括号和n个右括号的组合。

按顺序尝试知道左右括号都尝试完了就可以算作一个解。

__注意__：左括号的数不能大于右括号，要不然那就意味着先尝试了右括号而没有左括号，类似“)(” 这种解是不合法的。

### 解法

```java
public class Solution {
    public List<String> generateParenthesis(int n) {
        List<String> ans = new LinkedList<>();
        StringBuilder sample = new StringBuilder();

        dfs(ans, sample, n, n);
        return ans;
    }
    
    private void dfs(List<String> collection, StringBuilder sample, int left, int right) {
        if (left > right) {
            return;
        }

        if (left == 0 && right == 0) {
            collection.add(sample.toString());
            return;
        }

        if (left > 0) {
            sample.append('(');
            dfs(collection, sample, left - 1, right);
            int last = sample.length() - 1;
            sample.deleteCharAt(last);
        }

        if (right > 0) {
            sample.append(')');
            dfs(collection, sample, left, right - 1);
            int last = sample.length() - 1;
            sample.deleteCharAt(last);
        }
    }
}
```