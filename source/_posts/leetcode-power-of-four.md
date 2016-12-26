---
title: Power of Four
date: 2016-11-04 14:22:20
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 342

### 题目

判断一个数是否是4的幂次。

Given an integer (signed 32 bits), write a function to check whether it is a power of 4.

__Example__:

Given num = 16, return true. Given num = 5, return false.

__Follow up__: Could you solve it without loops/recursion?

### 分析

网上比较流行的一种解法，思路很巧妙，首先根据[Power of Two](/2016/11/01/leetcode-power-of-two/)中的解法二，我们知道`num & (num - 1)`可以用来判断一个数是否为2的次方数，更进一步说，就是二进制表示下，只有最高位是1，那么由于是2的次方数，不一定是4的次方数，比如8，所以我们还要其他的限定条件，我们仔细观察可以发现，4的次方数的最高位的1都是计数位，那么我们只需与上一个数`(0x55555555)` <==> `1010101010101010101010101010101`，如果得到的数还是其本身，则可以肯定其为4的次方数。

### 解法

```java
public class Solution {
    public boolean isPowerOfFour(int num) {
        return num > 0 && ((num & (num - 1)) == 0) && ((num & 0x5555555555555555L) == num);
    }
}
```