---
title: 随机红包
date: 2016-07-29 22:04:02
categories: 学术
tags: Leetcode
toc: true
---

一道普通的面试题。

### 题目

100块的红包，分给10个人，要求每个人能随机分到6至12块之间。

### 分析

开始打算递归、剪枝，但发现效果不好。

直接生成9个随机数，第10个数为`100 - sum`。

如果余数复合要求，即是答案。

### 答案

```python
# -*- coding: utf-8 -*-

import random


def bonus(total, arr, pos):
    s = 0
    while s != total:
        for i in xrange(pos):
            arr[i] = get_value()
            s += arr[i]
        if is_valid(total - sum(arr)):
            arr[pos] = total - sum(arr)
            s = total


def get_value():
    return round(random.uniform(6, 12), 2)


def is_valid(_):
    return 6.00 <= _ <= 12.0


if __name__ == '__main__':
    arr = 10 * [0.00]

    bonus(100.0, arr, 9)

    for v in arr:
        print v
```