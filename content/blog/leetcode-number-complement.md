+++
date = "2017-06-01T09:41:38+08:00"
title = "Number Complement"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 476"
slug = "leetcode-number-complement"
+++

### 题目

给出任意一个数字的补码。

Given a positive integer, output its complement number. The complement strategy is to flip the bits of its binary representation.

__Note__:

1. The given integer is guaranteed to fit within the range of a 32-bit signed integer.
2. You could assume no leading zero bit in the integer’s binary representation.

__Example 1__:

```console
Input: 5
Output: 2
Explanation: The binary representation of 5 is 101 (no leading zero bits), and its complement is 010. So you need to output 2.
```

__Example 2__:

```console
Input: 1
Output: 0
Explanation: The binary representation of 1 is 1 (no leading zero bits), and its complement is 0. So you need to output 0.
```

### 分析

用一个mask来标记最高位1前面的所有0的位置，然后对mask取反后，与上对num取反的结果，即可。

```console
num          = 00000101
mask         = 11111000
~mask & ~num = 00000010
```

### 解法

```go
func findComplement(num int) int {
    mask := ^0
    for (mask & num) > 0 {
        mask <<= 1
    }
    return ^mask & ^num
}
```
