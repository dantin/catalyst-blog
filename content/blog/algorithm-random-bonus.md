+++
date = "2016-07-29T22:04:02+08:00"
title = "随机红包问题"
categories = ["Scholar"]
tags = ["Algorithm"]
description = "本文记录红包问题的分析过程"
slug = "algorithm-random-bonus"
+++

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