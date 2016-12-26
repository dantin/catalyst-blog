---
title: Guess Number Higher or Lower
date: 2016-11-14 23:41:04
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 374

### 题目

判断数字大小。

We are playing the Guess Game. The game is as follows:

I pick a number from 1 to n. You have to guess which number I picked.

Every time you guess wrong, I'll tell you whether the number is higher or lower.

You call a pre-defined API guess(int num) which returns 3 possible results (-1, 1, or 0):

```
-1 : My number is lower
 1 : My number is higher
 0 : Congrats! You got it!
```

__Example__:

```
n = 10, I pick 6.

Return 6.
```

### 分析

二分查找，注意效率。

### 解法

```java
/* The guess API is defined in the parent class GuessGame.
   @param num, your guess
   @return -1 if my number is lower, 1 if my number is higher, otherwise return 0
      int guess(int num); */

public class Solution extends GuessGame {
    public int guessNumber(int n) {
        int low = 1;
        int high = n;
        while(low <= high) {
            int mid = (low + high) >>> 1;
            switch(guess(mid)) {
                case -1:
                    high = mid - 1;
                    break;
                case 1:
                    low = mid + 1;
                    break;
                default:
                    return mid;
            }
        }
        return low;
    }
}
```