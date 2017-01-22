+++
tags = ["Leetcode"]
date = "2017-01-22T15:16:58+08:00"
title = "Lexicographical Numbers"
description = "Leetcode 386"
slug = "leetcode-lexicographical-numbers"
categories = ["Code"]
+++

### 题目

给出一个整数$n$，把区间$[1,n]$的所有数字按照字典顺序来排列。

Given an integer $n$, return $1 - n$ in lexicographical order.

For example, given $13$, return: $[1,10,11,12,13,2,3,4,5,6,7,8,9]$.

Please optimize your algorithm to use less time and space. The input size may be as large as 5,000,000.

### 分析

按个位数遍历，在遍历下一个个位数之前，先遍历十位数，十位数的高位为之前的个位数，只要这个多位数并没有超过n，就可以一直往后遍历，如果超过了，我们除以10，然后再加1，如果加1后末尾形成了很多0，那么我们要用个while循环把0都去掉，然后继续运算。

### 解法

非递归

```java
public class Solution {
    public List<Integer> lexicalOrder(int n) {
        List<Integer> ans = new LinkedList<>();
        int cur = 1;
        for (int i = 0; i < n; i++) {
            ans.add(cur);
            if (cur * 10 <= n) {
                cur *= 10;
            } else {
                if (cur >= n) cur /= 10;
                cur += 1;
                while (cur % 10 == 0) cur /= 10;
            }
        }
        return ans;
    }
}
```

递归

```java
public class Solution {
    public List<Integer> lexicalOrder(int n) {
        List<Integer> ans = new LinkedList<>();
        for (int i = 1; i < 10; i++) {
            lexial(i, n, ans);
        }
        return ans;
    }

    private void lexial(int cur, int n, List<Integer> ans) {
        if (cur > n) return;
        ans.add(cur);
        for (int i = 0; i < 10; i++) {
            int num = cur * 10 + i;
            if (num > n) break;
            lexial(num, n, ans);
        }
    }
}
```