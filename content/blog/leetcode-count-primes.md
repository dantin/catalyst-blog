+++
date = "2016-11-25T23:06:14+08:00"
title = "Count Primes"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 204"
slug = "leetcode-count-primes"
+++

### 题目

计算某一范围内的质数个数。

Count the number of prime numbers less than a non-negative number, n.

### 分析

使用[Sieve of Eratosthenes算法](http://en.wikipedia.org/wiki/Sieve_of_Eratosthenes)。

创建长度为n的boolean数组，依次标记偶数、3的倍数、5的倍数...直到sqrt(n)为止。

剩下的未标记的数组即为质数的个数。

### 解法

```java
public class Solution {
    public int countPrimes(int n) {
        boolean[] isPrime = new boolean[n];
        for(int i = 2; i < n; i++) {
            isPrime[i] = true;
        }

        for(int i = 2; i * i < n; i++) {
            if(!isPrime[i]) continue;
            for(int j = i * i; j < n ; j += i) {
                isPrime[j] = false;
            }
        }

        int count = 0;
        for(int i = 2; i < n; i++) {
            if(isPrime[i]) {
                count++;
            }
        }
        return count;
    }
}
```