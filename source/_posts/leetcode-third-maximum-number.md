---
title: Third Maximum Number
date: 2016-11-24 18:33:20
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 414

### 题目

找数组中第三大的数。

Given a non-empty array of integers, return the third maximum number in this array. If it does not exist, return the maximum number. The time complexity must be in O(n).

__Example 1__:

```
Input: [3, 2, 1]

Output: 1

Explanation: The third maximum is 1.
```

__Example 2__:

```
Input: [1, 2]

Output: 2

Explanation: The third maximum does not exist, so the maximum (2) is returned instead.
```

__Example 3__:

```
Input: [2, 2, 3, 1]

Output: 1

Explanation: Note that the third maximum here means the third maximum distinct number.
Both numbers with value 2 are both considered as second maximum.
```

### 分析

利用变量a, b, c分别记录数组第1,2,3大的数字

遍历一次数组即可，时间复杂度O(n)

### 解法

```java
public class Solution {
    public int thirdMax(int[] nums) {
        Integer a = nums[0], b = null, c = null;

        for(int i = 1; i < nums.length; i++) {
            if((a != null && nums[i] == a) || 
                (b != null && nums[i] == b) ||
                (c != null && nums[i] == c))
                continue;
            if(a == null || nums[i] > a) {
                c = b;
                b = a;
                a = nums[i];
            } else if(b == null || nums[i] > b) {
                c = b;
                b = nums[i];
            } else if(c == null || nums[i] > c) {
                c = nums[i];
            }
        }

        if(c != null) return c;
        if(b != null) return a;
        return a;
    }
}
```