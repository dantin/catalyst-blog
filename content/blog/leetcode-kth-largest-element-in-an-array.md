+++
description = "Leetcode 215"
slug = "leetcode-kth-largest-element-in-an-array"
date = "2017-02-07T10:21:36+08:00"
title = "Kth Largest Element in an Array"
categories = ["Code"]
tags = ["Leetcode"]
+++

### 题目

从一个未经排序的数组中找出第k大的元素。注意是排序之后的第k大，而非第k个不重复的元素。

Find the kth largest element in an unsorted array. Note that it is the kth largest element in the sorted order, not the kth distinct element.

For example,

Given $[3,2,1,5,6,4]$ and $k = 2$, return $5$.

__Note__:

You may assume $k$ is always valid, 1 ≤ k ≤ array's length.

### 分析

$O(n)$解法：快速选择（QuickSelect）算法，参考耶鲁大学关于QuickSelect算法的介绍

$O(nlogn)$解法：排序

### 解法

排序：

```java
public class Solution {
    public int findKthLargest(int[] nums, int k) {
        Arrays.sort(nums);

        return nums[nums.length - k];
    }
}
```

堆排序：

```java
public class Solution {
    public int findKthLargest(int[] nums, int k) {
        PriorityQueue<Integer> heap = new PriorityQueue<>();
        for (int x : nums) {
            heap.offer(x);
            if (heap.size() > k) {
                heap.poll();
            }
        }
        return heap.peek();
    }
}
```

快速选择算法：

```java
public class Solution {
    public int findKthLargest(int[] nums, int k) {
        return quickSelect(nums, nums.length - k + 1, 0, nums.length - 1);
    }

    private int quickSelect(int[] nums, int k, int low, int high) {
        int pivot = nums[high];

        int left = low;
        int right = high;

        while (true) {
            while (nums[left] < pivot && left < right) left++;
            while (nums[right] >= pivot && right > left) right--;
            if (left == right) break;
            swap(nums, left, right);
        }
        swap(nums, left, high);

        if (left + 1 == k)
            return pivot;
        else if (k < left + 1)
            return quickSelect(nums, k, low, left - 1);
        else
            return quickSelect(nums, k, left + 1, high);
    }

    private void swap(int[] nums, int i, int j) {
        int tmp = nums[i];
        nums[i] = nums[j];
        nums[j] = tmp;
    }
}
```