+++
date = "2016-12-08T18:21:50+08:00"
title = "Top K Frequent Elements"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 347"
slug = "leetcode-top-k-frequent-elements"
+++

### 题目

取数组中出现频次最高的K个元素。

Given a non-empty array of integers, return the k most frequent elements.

For example,

Given $[1,1,1,2,2,3]$ and k = 2, return $[1,2]$.

__Note__:

* You may assume k is always valid, 1 ≤ k ≤ number of unique elements.
* Your algorithm's time complexity must be better than O(n log n), where n is the array's size.

### 分析

统计词频，构造最小堆即可。

### 解法

```java
public class Solution {
    public List<Integer> topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> freq = new HashMap<>();
        for(int num : nums) {
            if(freq.containsKey(num)) {
                int cnt = freq.get(num);
                freq.put(num, cnt+1);
            } else {
                freq.put(num, 1);
            }
        }

        Queue<Pair> heap = new PriorityQueue<>(new Comparator<Pair>() {
            @Override
            public int compare(Pair o1, Pair o2) {
                return o1.freq - o2.freq;
            }
        });

        int count = 0;
        for(Map.Entry<Integer, Integer> entry : freq.entrySet()) {
            Pair pair = new Pair(entry.getKey(), entry.getValue());
            if(count < k) {
                heap.offer(pair);
            } else if(pair.freq > heap.peek().freq) {
                heap.poll();
                heap.offer(pair);
            }
            count++;
        }

        List<Integer> top = new ArrayList<>();
        for(Pair node : heap) {
            top.add(node.value);
        }
        Collections.reverse(top);
        return top;
    }
    
    class Pair {
        int value;
        int freq;
        Pair(int value, int freq) {
            this.value = value;
            this.freq = freq;
        }
    }
}
```
