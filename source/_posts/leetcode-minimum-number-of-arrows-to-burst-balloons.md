---
title: Minimum Number of Arrows to Burst Balloons
date: 2016-12-23 14:40:03
categories: 练习
tags: Leetcode
toc: true
mathjax: true
---

Leetcode 452

### 题目

使用最少数量的箭引爆气球。

There are a number of spherical balloons spread in two-dimensional space. For each balloon, provided input is the start and end coordinates of the horizontal diameter. Since it's horizontal, y-coordinates don't matter and hence the x-coordinates of start and end of the diameter suffice. Start is always smaller than end. There will be at most $10^4$ balloons.

An arrow can be shot up exactly vertically from different points along the x-axis. A balloon with xstart and xend bursts by an arrow shot at x if xstart ≤ x ≤ xend. There is no limit to the number of arrows that can be shot. An arrow once shot keeps travelling up infinitely. The problem is to find the minimum number of arrows that must be shot to burst all balloons.

__Example__:

```
Input:
[[10,16], [2,8], [1,6], [7,12]]

Output:
2

Explanation:
One way is to shoot one arrow for example at x = 6 (bursting the balloons [2,8] 
and [1,6]) and another arrow at x = 11 (bursting the other two balloons).
```

### 分析

贪婪算法。局部最优解就等于全局最优解。

首先给区间排序，按第一个数字升序排列，如果第一个数字相同，那么按第二个数字升序排列。

然后将count初始化为1，因为气球数量不为0，所以不论如何都需要一箭，然后这一箭能覆盖的最远位置就是第一个气球的结束点，用变量end来表示。然后开始遍历剩下的气球，如果当前气球的开始点小于等于end，说明跟之前的气球有重合，之前那一箭也可以照顾到当前的气球，此时我们要更新end的位置，end更新为两个气球结束点之间较小的那个，这也是当前气球和之前气球的重合点，然后继续看后面的气球；如果某个气球的起始点大于end了，说明前面的箭无法覆盖到当前的气球，那么就得再补一箭，既然又来了一箭，那么此时就要把end设为当前气球的结束点了。

这样贪婪算法遍历结束后就能得到最少的箭数。

### 解法

```java
public class Solution {
    public int findMinArrowShots(int[][] points) {
        if (points == null || points.length == 0) return 0;
        // sort by begin, then end
        Arrays.sort(points, (x, y) -> x[0] == y[0] ? x[1] - y[1] : x[0] - y[0]);
        int count = 1;
        int end = points[0][1];
        for (int i = 1; i < points.length; i++) {
            if (points[i][0] <= end) {
                end = Math.min(end, points[i][1]);
            } else {
                count++;
                end = points[i][1];
            }
        }
        return count;
    }
}
```