---
title: Sum of Two Integers
date: 2016-10-20 14:12:25
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 371

### 题目

不用加减乘除运算来计算两数的和。

Calculate the sum of two integers a and b, but you are not allowed to use the operator + and -.

Example:
Given a = 1 and b = 2, return 3.

### 分析

以`10(1010) + 25(11001)`

如果`1010 + 0101 = 1111`在计算上不产生进位，则`1010 + 0101 = 1010 ^ 0101 = 1111`

上面1010和0101二进制加法计算的特点是没有进位，它们的二进制加法和按位异或运算结果相同。但如果是二进制加法运算有进位，则以上等价关系就不能成立。
 
思路：如`20(10100) + 25(11001) = 45`二进制加法运算会产生进位，那么把它转换成a和b两个数，满足`a + b = 20 + 25 = 45`且a和b二进制加法不会产生进位。
 
那么如何找到a和b呢？

当产生进位的时候，我们可以试着把产生进制的位置找出来，20(10100)+25(11001)进行按位与运算`10100 & 11001 = 10000`可知道在最高位是两个1相与，故在最高位产生进位。`10100 ^ 11001 = 01101`这个结果是不进位的结果，只要我们把不进位的异或运算加上进位时候带来的结果增量加起来，就是我们最终想要的结果，`10100 + 11001 = 101101`。

推导过程为：

```
10100 + 11001 = 10100 ^ 11001 +（10100&11001）<<1
              = 01101 + 10000 <<1

a =  01101
b =  10000 <<1 = 100000  // 左移位后的结果即为进位产生的增量
```

如果a、b还不满足上面思路中的要求的话，需要重复上面的过程，直到找出满足思路中的a、b的值。

### 解法

非递归

```java
public class Solution {
    public int getSum(int a, int b) {
        while(b != 0) {
            int carry = a & b;  // CARRY is AND of two bits
            a = a ^ b;          // SUM of two bits is A XOR B
            b = carry << 1;     // shifts carry to 1 bit to calculate sum
        }
        return a;
    }
}
```

递归

```java
public class Solution {
    public int getSum(int a, int b) {
        if(b == 0) return a;
        int sum = a ^ b;           //SUM of two integer is A XOR B
        int carry = (a & b) << 1;  //CARRY of two integer is A AND B
        return add(sum, carry);
    }
}
```
