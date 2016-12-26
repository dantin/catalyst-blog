---
title: Contains Duplicate II
date: 2016-11-19 22:46:31
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 219

### 题目

判断一定步长内的字符串是否存在重复字符。

Given an array of integers and an integer k, find out whether there are two distinct indices i and j in the array such that nums[i] = nums[j] and the difference between i and j is at most k.

### 分析

使用滑动窗口，每次近来一个数前先删掉i-k-1位置的数，然后判断是否有重复字符。

### 解法

简单做法：

```java
public class Solution {
    public boolean containsDuplicate(int[] nums, int k) {
        Deque<Integer> fifo = new LinkedList<>();

        for(int i = 0; i < nums.length; i++) {
            int num = nums[i];

            if(i > k) {
                fifo.removeFirst();
            }

            if(fifo.contains(num)) return true;
            fifo.addLast(num);
        }

        return false;
    }
}
```

上述做法会超时，优化使用HashMap。

```java
public class Solution {
    public boolean containsNearbyDuplicate(int[] nums, int k) {
        Map<Integer, Integer> freqs = new HashMap<>();

        for(int i = 0; i < nums.length; i++) {
            int num = nums[i];
            int freq = 0;

            if(i > k) {
                int out = nums[i - k - 1];
                freq = freqs.getOrDefault(out, 0);
                if(--freq == 0) {
                    freqs.remove(out);
                } else {
                    freqs.put(out, freq);
                }
            }
            
            if(freqs.containsKey(num)) {
                freq = freqs.get(num);
                freqs.put(num, ++freq);
                if(freq > 1) return true;
            } else {
                freqs.put(num, 1);
            }
        }

        return false;
    }
}
```

Map中的频次其实用处不大，用Set优化：

```java
public class Solution {
    public boolean containsNearbyDuplicate(int[] nums, int k) {
        Set<Integer> set = new HashSet<>();

        for(int i = 0; i < nums.length; i++) {
            int num = nums[i];

            if(i > k) {
                set.remove(nums[i - k - 1]);
            }

            if(set.contains(num)) return true;
            set.add(num);
        }

        return false;
    }
}
```