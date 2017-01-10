+++
date = "2016-12-06T14:38:21+08:00"
title = "Two Sum II - Input array is sorted"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 167"
slug = "leetcode-two-sum-ii-input-array-is-sorted"
+++

### 题目

找出和为某数的下标。

Given an array of integers that is already __sorted in ascending order__, find two numbers such that they add up to a specific target number.

The function twoSum should return indices of the two numbers such that they add up to the target, where index1 must be less than index2. Please note that your returned answers (both index1 and index2) are not zero-based.

You may assume that each input would have exactly one solution.

```console
Input: numbers={2, 7, 11, 15}, target=9
Output: index1=1, index2=2
```

### 分析

二分法，因为一定有解，而且数组是有序的，那么第一个数字肯定要小于目标值target，那么我们每次用二分法来搜索$target - numbers[i]$即可，复杂度：$O(N*\log N)$。

两个指针，一个指向开头，一个指向末尾，然后向中间遍历，如果指向的两个数相加正好等于target的话，直接返回两个指针的位置即可，若小于target，左指针右移一位，若大于target，右指针左移一位，以此类推直至两个指针相遇停止。

### 解法

方法一：

```java
public class Solution {
    public int[] twoSum(int[] nums, int target) {
        for(int i = 0; i < nums.length; i++) {
            int t = target - nums[i];
            int low = i + 1, high = nums.length - 1;
            while(low < high) {
                int mid = (low + high) / 2;
                if(t == nums[mid]) return new int[]{i+1, mid+1};
                else if(nums[mid] < t) low = mid + 1;
                else high = mid;
            }
        }
        return new int[2];
    }
}
```

方法二：

```java
public class Solution {
    public int[] twoSum(int[] numbers, int target) {
        int low = 0, high = numbers.length - 1;
        while(low < high) {
            int sum = numbers[low] + numbers[high];
            if(sum == target) return new int[]{low+1, high+1};
            else if(sum < target) low++;
            else high--;
        }
        return new int[2];
    }
}
```