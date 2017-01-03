---
title: House Robber
date: 2016-11-04 15:09:39
categories: 练习
tags: Leetcode
toc: true
mathjax: true
---

Leetcode 198

### 题目

查看最大可能的抢劫数量，不能相邻取。

You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security system connected and __it will automatically contact the police if two adjacent houses were broken into on the same night__.

Given a list of non-negative integers representing the amount of money of each house, determine the maximum amount of money you can rob tonight __without alerting the police__.

### 分析

采用动态规划，通项公式为：

{% math %}
\begin{aligned}
\text{Let array: $a_0$, $a_1$, $\dots$, $a_n$}\\
\\
F(n) = \max \begin{cases}
F(n-2) + a_n \\[2ex]
F(n-1)
\end{cases}
\end{aligned}
{% endmath %}


### 解法

解法一：

```java
public class Solution {
    public int rob(int[] nums) {
        if (nums.length <= 1) return nums.length == 0 ? 0 : nums[0];
        LinkedList<Integer> dp = new LinkedList<>();
        dp.add(nums[0]);
        dp.add(Math.max(nums[0], nums[1]));
        for (int i = 2; i < nums.length; i++) {
            dp.add(Math.max(nums[i] + dp.get(i - 2), dp.peekLast()));
        }
        return dp.peekLast();
    }
}
```

解法二，按奇偶更新：

```java
public class Solution {
    public int rob(int[] nums) {
        int odd = 0, even = 0;
        for (int i = 0; i < nums.length; i++) {
            if (i % 2 == 0) {
                even += nums[i];
                even = Math.max(odd, even);
            } else {
                odd += nums[i];
                odd = Math.max(odd, even);
            }
        }
        return Math.max(odd, even);
    }
}
```

解法三：

```java
public class Solution {
    public int rob(int[] nums) {
        int ans = 0;
        int hist = 0, pre = 0;
        for (int i = 0; i < nums.length; i++) {
            ans = Math.max(hist + nums[i], pre);
            hist = pre;
            pre = ans;
        }

        return Math.max(ans, pre);
    }
}
```