+++
title = "Gray Code"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 89"
slug = "leetcode-gray-code"
date = "2017-01-23T11:36:17+08:00"
+++

### 题目

找出给定长度的所有格雷码。

The gray code is a binary numeral system where two successive values differ in only one bit.

Given a non-negative integer n representing the total number of bits in the code, print the sequence of gray code. A gray code sequence must begin with 0.

For example, given $n = 2$, return $[0,1,3,2]$. Its gray code sequence is:

```console
00 - 0
01 - 1
11 - 3
10 - 2
```

__Note__:

For a given n, a gray code sequence is not uniquely defined.

For example, $[0,2,3,1]$ is also a valid gray code sequence according to the above definition.

For now, the judge is able to judge based on one instance of gray code sequence. Sorry about that.

### 分析

__思路一__

递归，利用格雷码的特性。

n位的格雷码由两部分构成，一部分是`n-1`位格雷码，再加上`1<<(n-1)`和`n-1`位格雷码的逆序的和。

例如：

当`n=1`时，格雷码：

```console
0
1
```

当`n=2`时，原来的结果$[0, 1]$不变，只是前面形式上加了个0变成$[00, 01]$。然后加数是`1<<1`为$10$，依次：$10+1=11, 10+0=10$。结果为：

```console
00
01
11
10
```

当`n=3`时，原来的结果$[00, 01, 11, 10]$（倒序为：$[10, 11, 01, 00]$）。加数`1<<2`为$100$。倒序相加为：$100+10=110, 100+11=111, 100+01=101, 100+00=100$。最终结果为：

```console
000
001
011
010
110
111
101
100
```

__思路二__

工业中的第i个格雷码是这么生成的：

```c
(i>>1)^i
```

i是指下标，从0开始，对于n的格雷码序列，一共有2^n个数

### 解法

思路一：

```java
public class Solution {
    public List<Integer> grayCode(int n) {
        List<Integer> ans = null;
        if (n == 0) {
            ans = new LinkedList<>();
            ans.add(0);
            return ans;
        }

        ans = grayCode(n - 1);
        int weight = 1 << (n - 1);
        int size = ans.size();

        for (int i = size - 1; i >= 0; i--) {
            ans.add(weight + ans.get(i));
        }

        return ans;
    }
}
```

思路二：

```java
public class Solution {
    public List<Integer> grayCode(int n) {
        List<Integer> ans = new LinkedList<>();

        for (int i = 0; i < (1 << n); i++) {
            ans.add((i >> 1) ^ i);
        }
        
        return ans;
    }
}
```