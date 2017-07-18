+++
title = "Next Greater Element I"
description = "Leetcode 496"
slug = "leetcode-next-greater-element-i"
categories = ["Code"]
tags = ["Leetcode"]
date = "2017-07-10T16:16:37+08:00"
+++

### 题目

找下一个大于它的整数。

You are given two arrays __(without duplicates)__ nums1 and nums2 where nums1’s elements are subset of nums2. Find all the next greater numbers for nums1's elements in the corresponding places of nums2.

The Next Greater Number of a number x in nums1 is the first greater number to its right in nums2. If it does not exist, output -1 for this number.

Example 1:

```console
Input: nums1 = [4,1,2], nums2 = [1,3,4,2].
Output: [-1,3,-1]
Explanation:
    For number 4 in the first array, you cannot find the next greater number for it in the second array, so output -1.
    For number 1 in the first array, the next greater number for it in the second array is 3.
    For number 2 in the first array, there is no next greater number for it in the second array, so output -1.
```

Example 2:

```console
Input: nums1 = [2,4], nums2 = [1,2,3,4].
Output: [3,-1]
Explanation:
    For number 2 in the first array, the next greater number for it in the second array is 3.
    For number 4 in the first array, there is no next greater number for it in the second array, so output -1.
```

Note:

* All elements in nums1 and nums2 are unique.
* The length of both nums1 and nums2 would not exceed 1000.

### 分析

这题其实就是个栈，如果当前元素小于栈顶元素，则压栈；

只有在当前元素大于栈顶元素是，才需要出栈，直到栈为空，或站定元素大于等于当前元素。

我们把这部分放到一个缓存里，然后输出结果即可。

比如：$[5, 4, 3, 2, 1, 6]$中，6是前五个的下一个大值。

再比如：$[9, 8, 7, 3, 2, 1, 6]$中，6是1、2、3的下一个大值。

### 解法

```go
func nextGreaterElement(findNums []int, nums []int) []int {
    cached := make(map[int]int)
    s := New()
    for _, num := range nums {
        for !s.IsEmpty() && s.Peek().(int) < num {
            cached[s.Pop().(int)] = num
        }

        s.Push(num)
    }

    nexted := make([]int, 0)
    for _, num := range findNums {
        t, ok := cached[num]
        if ok {
            nexted = append(nexted, t)
        } else {
            nexted = append(nexted, -1)
        }
    }

    return nexted
}

type Stack struct {
    top    *node
    length int
}

type node struct {
    value interface{}
    prev  *node
}

// Create a new stack
func New() *Stack {
    return &Stack{nil, 0}
}

// Return the number of items in the stack
func (s *Stack) Len() int {
    return s.length
}

// IsEmpty check whether a stack is empty
func (s *Stack) IsEmpty() bool {
    return s != nil && s.length == 0
}

// View the top item on the stack
func (s *Stack) Peek() interface{} {
    if s.length == 0 {
        return nil
    }
    return s.top.value
}

// Pop the top item of the stack and return it
func (s *Stack) Pop() interface{} {
    if s.length == 0 {
        return nil
    }

    n := s.top
    s.top = n.prev
    s.length--
    return n.value
}

// Push a value onto the top of the stack
func (s *Stack) Push(value interface{}) {
    n := &node{value, s.top}
    s.top = n
    s.length++
}
```

