+++
slug = "leetcode-non-overlapping-intervals"
categories = ["Code"]
tags = ["Leetcode"]
date = "2017-01-15T22:56:54+08:00"
title = "Non Overlapping Intervals"
description = "Leetcode 435"
+++

### 题目

假设有一组一堆时间序列区间，求需要至少移除多少个区间才能使剩下的区间没有重叠。

Given a collection of intervals, find the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.

__Note__:

1. You may assume the interval's end point is always bigger than its start point.
2. Intervals like $[1,2]$ and $[2,3]$ have borders "touching" but they don't overlap each other.

__Example 1__:

```console
Input: [ [1,2], [2,3], [3,4], [1,3] ]

Output: 1

Explanation: [1,3] can be removed and the rest of intervals are non-overlapping.
```

__Example 2__:

```console
Input: [ [1,2], [1,2], [1,2] ]

Output: 2

Explanation: You need to remove two [1,2] to make the rest of intervals non-overlapping.
```

__Example 3__:

```console
Input: [ [1,2], [2,3] ]

Output: 0

Explanation: You don't need to remove any of the intervals since they're already non-overlapping.
```

### 分析

首先给区间排序，根据每个区间的start来做升序排序；

查找重叠区间。判断方法：看如果前一个区间的end大于后一个区间的start，那么一定是重复区间，此时结果ans自增1，删除那个end值较大的区间，而在代码中，我们并没有真正的删掉某一个区间，而是用一个变量last指向上一个需要比较的区间，我们将last指向end值较小的那个区间；如果两个区间没有重叠，那么此时last指向当前区间，继续进行下一次遍历。

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
    public int eraseOverlapIntervals(Interval[] intervals) {
        int ans = 0, len = intervals.length, last = 0;
        Arrays.sort(intervals, 0, len, new Comparator<Interval>() {
            @Override
            public int compare(Interval o1, Interval o2) {
                return o1.start - o2.start;
            }
        });
        for (int i = 1; i < len; i++) {
            if (intervals[i].start < intervals[last].end) {
                ans++;
                if (intervals[i].end < intervals[last].end) last = i;
            } else {
                last = i;
            }
        }
        return ans;
    }
}
```
