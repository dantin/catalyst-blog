+++
date = "2016-10-24T10:46:43+08:00"
title = "Intersection of Two Arrays"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 349"
slug = "leetcode-intersection-of-two-arrays"
+++

### 题目

求两个数组的交集。

Given two arrays, write a function to compute their intersection.

Example:
Given nums1 = $[1, 2, 2, 1]$, nums2 = $[2, 2]$, return $[2]$.

Note:
Each element in the result must be unique.
The result can be in any order.

### 分析

构造集合，求交集。时间复杂度O(n * log(n))。

### 解法

```java
public class Solution {
    public int[] intersection(int[] nums1, int[] nums2) {
        Set<Integer> set1 = IntStream.of(nums1).boxed().collect(Collectors.toSet());
        Set<Integer> set2 = IntStream.of(nums2).boxed().collect(Collectors.toSet());
        set1.retainAll(set2);
        
        return set1.stream().mapToInt(Integer::intValue).toArray();
    }
}
```

使用java.util.BitSet，从0.21%提升到2.4%。

```java
public class Solution {
    public int[] intersection(int[] nums1, int[] nums2) {
        BitSet nb1 = new BitSet();
        BitSet nb2 = new BitSet();
        for(int i = 0; i < nums1.length; i++)
            nb1.set(nums1[i]);
        for(int i = 0; i < nums2.length; i++)
            nb2.set(nums2[i]);
        nb1.and(nb2);
        return nb1.stream().toArray();
    }
}
```

最原始的方法

```java
public class Solution {
    public int[] intersection(int[] nums1, int[] nums2) {
        Set<Integer> set = new HashSet<>();
        for(int i = 0; i < nums1.length; i++)
           set.add(nums1[i]);
        Set<Integer> r = new HashSet<>();
        for(int i = 0; i < nums2.length; i++)
           if(set.contains(nums2[i])) r.add(nums2[i]);
        
        return r.stream().mapToInt(Integer::intValue).toArray();
    }
}
```

发现瓶颈在最后一句。修改后，提升至77.92%

```java
public class Solution {
    public int[] intersection(int[] nums1, int[] nums2) {
        Set<Integer> set = new HashSet<>();
        for(int i = 0; i < nums1.length; i++)
            set.add(nums1[i]);
        Set<Integer> r = new HashSet<>();
        for(int i = 0; i < nums2.length; i++)
            if(set.contains(nums2[i])) r.add(nums2[i]);
        int[] result = new int[r.size()];
        int i = 0;
        for(Integer x : r) {
            result[i++] = x;
        }
        return result;
    }
}
```