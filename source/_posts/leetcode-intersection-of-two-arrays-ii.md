---
title: Intersection of Two Arrays II
date: 2016-10-28 14:04:05
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 350

### 题目

求两个数组的交集，可重复。

Given two arrays, write a function to compute their intersection.

__Example__:

Given nums1 = [1, 2, 2, 1], nums2 = [2, 2], return [2, 2].

__Note__:

* Each element in the result should appear as many times as it shows in both arrays.
* The result can be in any order.

__Follow up__:

* What if the given array is already sorted? How would you optimize your algorithm?
* What if nums1's size is small compared to nums2's size? Which algorithm is better?
* What if elements of nums2 are stored on disk, and the memory is limited such that you cannot load all elements into the memory at once?

### 分析

构造Map，求词频率。

### 解法

```java
public class Solution {
    public int[] intersect(int[] nums1, int[] nums2) {
        Map<Integer, Integer> freqMap = new HashMap<>();
        for(int x : nums1) {
            if(freqMap.containsKey(x)) {
                int count = freqMap.get(x);
                freqMap.put(x, count + 1);
            } else {
                freqMap.put(x, 1);
            }
        }
        List<Integer> intersection = new LinkedList<>();
        for(int x : nums2) {
            int count = 0;
            if((count = freqMap.getOrDefault(x, 0)) > 0) {
                intersection.add(x);
                freqMap.put(x, count - 1);
            }
        }

        int[] result = new int[intersection.size()];
        for(int i = 0; i < intersection.size(); i++) {
            result[i] = intersection.get(i);
        }
        return result;
    }
}
```