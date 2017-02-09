+++
description = "快速选择算法"
slug = "algorithm-quick-select"
date = "2017-02-08T11:08:20+08:00"
title = "快速选择算法"
categories = ["Scholar"]
tags = ["Algorithm"]
+++

对于一个没有排序的数组, 如何快速找到它的中位数?

以上这个问题的答案就在类似快速排序中的partition()函数.

partition()函数的返回值表示pivot在排序好的数组中的位置(rank), 这个消息非常有用: 

> 中值只不过是rank等于长度除以2的元素而已.

为了寻找rank等于k的元素, 我们用partition函数可以每次把问题规模缩小: 

如果partition()=pk那么右边subarray不用考虑, 如果数组事先shuffle过了的话, 问题规模每次缩小一半.

定义一个函数, 寻找rank等于k的元素, 代码类似于二分查找:

```python
import random
class Solution:
    # @param {integer[]} nums
    # @param {integer} k
    # @return {integer}
    def findKthLargest(self, nums, k):
        pivot = random.choice(nums)
        nums1, nums2 = [], []
        for num in nums:
            if num > pivot:
                nums1.append(num)
            elif num < pivot:
                nums2.append(num)
        if k <= len(nums1):
            return self.findKthLargest(nums1, k)
        if k > len(nums) - len(nums2):
            return self.findKthLargest(nums2, k - (len(nums) - len(nums2)))
        return pivot
```

该算法内层循环为O(hi-lo), 每次问题规模减少一半, 所以复杂度为N+N/2+N/4+...+1 = 2N, 复杂度为线性时间!

参考：[耶鲁大学关于QuickSelect算法的介绍](http://www.cs.yale.edu/homes/aspnes/pinewiki/QuickSelect.html)
