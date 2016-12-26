---
title: Bulls and Cows
date: 2016-11-15 00:05:58
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 299

### 题目

判断出现的相同字符。

You are playing the following [Bulls and Cows](https://en.wikipedia.org/wiki/Bulls_and_Cows) game with your friend: You write down a number and ask your friend to guess what the number is. Each time your friend makes a guess, you provide a hint that indicates how many digits in said guess match your secret number exactly in both digit and position (called "bulls") and how many digits match the secret number but locate in the wrong position (called "cows"). Your friend will use successive guesses and hints to eventually derive the secret number.

For example:

```
Secret number:  "1807"
Friend's guess: "7810"
```

Hint: 1 bull and 3 cows. (The bull is 8, the cows are 0, 1 and 7.)

Write a function to return a hint according to the secret number and friend's guess, use A to indicate the bulls and B to indicate the cows. In the above example, your function should return "1A3B".

Please note that both secret number and friend's guess may contain duplicate digits, for example:

```
Secret number:  "1123"
Friend's guess: "0111"
```

In this case, the 1st 1 in friend's guess is a bull, the 2nd or 3rd 1 is a cow, and your function should return "1A1B".

You may assume that the secret number and your friend's guess only contain digits, and their lengths are always equal.

### 分析

按位置异或，找出相同位置相同字符的bull，同时构造字符频率表；扫guess出结果。

### 解法

```java
public class Solution {
    public String getHint(String secret, String guess) {
        int[] cache = new int[10];

        int bull = 0;
        int cow = 0;
        char[] sa = secret.toCharArray();
        char[] ga = guess.toCharArray();

        for(int i = 0; i < sa.length; i++) {
            if((sa[i] ^ ga[i]) == 0) bull++;
            cache[sa[i] - '0']++;
        }

        for(char c : ga) {
            if(cache[c - '0']-- > 0) cow++;
        }
        return String.format("%dA%dB", bull, cow - bull);
    }
}
```