---
title: Heaters
date: 2016-12-20 22:39:22
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 475

### 题目

求加热器辐射热量的最小距离。

Winter is coming! Your first job during the contest is to design a standard heater with fixed warm radius to warm all the houses.

Now, you are given positions of houses and heaters on a horizontal line, find out minimum radius of heaters so that all houses could be covered by those heaters.

So, your input will be the positions of houses and heaters seperately, and your expected output will be the minimum radius standard of heaters.

__Note__:

1. Numbers of houses and heaters you are given are non-negative and will not exceed 25000.
2. Positions of houses and heaters you are given are non-negative and will not exceed 10^9.
3. As long as a house is in the heaters' warm radius range, it can be warmed.
4. All the heaters follow your radius standard and the warm radius will the same.

__Example 1__:

```
Input: [1,2,3],[2]
Output: 1
Explanation: The only heater was placed in the position 2, and if we use the radius 1 standard, then all the houses can be warmed.
```

__Example 2__:

```
Input: [1,2,3,4],[1,4]
Output: 1
Explanation: The two heater was placed in the position 1 and 4. We need to use radius 1 standard, then all the houses can be warmed.
```

### 分析

这道题目先对加热器排序，用二分查找法来快速找到第一个大于等于当前house位置的加热器位置，如果这个加热器存在，那么算出house和前一个加热器及当前加热器位置的差值。

这两个数中较小的为cover当前house的最小半径，每次更新结果即可。

注意：找到的加热器位置是第一个及最后一个的处理。

### 解法

```java
public class Solution {
    public int findRadius(int[] houses, int[] heaters) {
        int ans = 0;
        Arrays.sort(heaters);
        for(int house : houses) {
            int left = 0, right = heaters.length;
            while(left < right) {
                int mid = (left + right) / 2;
                if(heaters[mid] < house) left = mid + 1;
                else right = mid;
            }
            int right_radius = (right == heaters.length) ? Integer.MAX_VALUE : heaters[right] - house;
            int left_radius = (right == 0) ? Integer.MAX_VALUE : house - heaters[right - 1];
            ans = Math.max(ans, Math.min(left_radius, right_radius));
        }
        return ans;
    }
}
```