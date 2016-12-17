---
title: Find Right Interval
date: 2016-12-17 23:07:34
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 436

### 题目

给一组区间，对于每一个区间i，检查是否存在区间j，满足j的起点大于等于i的终点，我们称j在i的“右边"。

对于任意区间i，你需要存储j的最小下标，这意味着区间j拥有最小的起点并且位于i的“右边”。如果j不存在，则存储为-1。将最终结果以数组形式返回。

Given a set of intervals, for each of the interval i, check if there exists an interval j whose start point is bigger than or equal to the end point of the interval i, which can be called that j is on the "right" of i.

For any interval i, you need to store the minimum interval j's index, which means that the interval j has the minimum start point to build the "right" relationship for interval i. If the interval j doesn't exist, store -1 for the interval i. Finally, you need output the stored value of each interval as an array.

__Note__:

* You may assume the interval's end point is always bigger than its start point.
* You may assume none of these intervals have the same start point.

__Example 1__:

```
Input: [ [1,2] ]

Output: [-1]

Explanation: There is only one interval in the collection, so it outputs -1.
```

__Example 2__:

```
Input: [ [3,4], [2,3], [1,2] ]

Output: [-1, 0, 1]

Explanation: There is no satisfied "right" interval for [3,4].
For [2,3], the interval [3,4] has minimum-"right" start point;
For [1,2], the interval [2,3] has minimum-"right" start point.
```

__Example 3__:

```
Input: [ [1,4], [2,3], [3,4] ]

Output: [-1, 2, -1]

Explanation: There is no satisfied "right" interval for [1,4] and [3,4].
For [2,3], the interval [3,4] has minimum-"right" start point.
```

### 分析

排序（Sort）+ 二分查找（Binary Search）

按照区间起点排序，然后二分查找比i大的最小值即可。

实现时利用TreeMap。

### 解法

```java
/**
 * Definition for an interval.
 * public class Interval {
 *     int start;
 *     int end;
 *     Interval() { start = 0; end = 0; }
 *     Interval(int s, int e) { start = s; end = e; }
 * }
 */
public class Solution {
    public int[] findRightInterval(Interval[] intervals) {
        if(intervals == null || intervals.length == 0) return null;

        int[] ans = new int[intervals.length];
        java.util.NavigableMap<Integer, Integer> map = new TreeMap<>();
        for(int i = 0; i < intervals.length; i++) {
            map.put(intervals[i].start, i);
        }
        for(int i = 0; i < intervals.length; i++) {
            Map.Entry<Integer, Integer> target = map.ceilingEntry(intervals[i].end);
            ans[i] = (target == null) ? -1 : target.getValue();
        }
        return ans;
    }
}
```