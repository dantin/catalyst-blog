+++
date = "2016-10-27T11:50:56+08:00"
title = "Majority Element"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 169"
slug = "leetcode-majority-element"
+++

### 题目

给定一个长度为n的数组，寻找其中的“众数”。众数是指出现次数大于 ⌊ n/2 ⌋ 的元素。

Given an array of size n, find the majority element. The majority element is the element that appears more than ⌊ n/2 ⌋ times.

You may assume that the array is non-empty and the majority element always exist in the array.

### 分析

“投票算法”，设定两个变量candidate和count。candidate保存当前可能的候选众数，count保存该候选众数的出现次数。

遍历数组num。

如果当前的数字e与候选众数candidate相同，则将计数count + 1

否则，如果当前的候选众数candidate为空，或者count为0，则将候选众数candidate的值置为e，并将计数count置为1。

否则，将计数count - 1

最终留下的候选众数candidate即为最终答案。

以上算法时间复杂度为O(n)，空间复杂度为O(1)。

### 解法

```java
public class Solution {
    public int majorityElement(int[] nums) {
        int candidate = nums[0];
        int count = 1;
        for(int i = 1; i < nums.length; i++) {
            if(candidate == nums[i]) {
                count++;
            } else {
                count--;
                if(count == 0) {
                    candidate = nums[i];
                    count = 1;
                }
            }
        }
        return candidate;
    }
}
```