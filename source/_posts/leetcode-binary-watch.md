---
title: Binary Watch
date: 2016-10-28 14:51:29
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 401

### 题目

根据输入求二进制表可能的情况。

A binary watch has 4 LEDs on the top which represent the hours (0-11), and the 6 LEDs on the bottom represent the minutes (0-59).

Each LED represents a zero or one, with the least significant bit on the right.

![二进制表](/images/Binary_clock_samui_moon.jpg "Binary Watch")

For example, the above binary watch reads "3:25".

Given a non-negative integer n which represents the number of LEDs that are currently on, return all possible times the watch could represent.

__Example__:

```
Input: n = 1
Return: ["1:00", "2:00", "4:00", "8:00", "0:01", "0:02", "0:04", "0:08", "0:16", "0:32"]
```

__Note__:

* The order of output does not matter.
* The hour must not contain a leading zero, for example "01:00" is not valid, it should be "1:00".
* The minute must be consist of two digits and may contain a leading zero, for example "10:2" is not valid, it should be "10:02".

### 分析

穷举，求结果。

### 解法

```java
public class Solution {
    public List<String> readBinaryWatch(int num) {
        List<String> times = new LinkedList<>();
        for(int h = 0; h < 12; h++) {
            for(int m = 0; m < 60; m++) {
                StringBuilder bits = new StringBuilder();
                bits.append(Integer.toBinaryString(h)).append(Integer.toBinaryString(m));
                int size = 0;
                for(int i = 0; i < bits.length(); i++) {
                    if(bits.charAt(i) == '1') {
                        size ++;
                    }
                }
                if(size == num) {
                    times.add(String.format("%d:%02d", h, m));
                }
            }
        }
        return times;
    }
}
```