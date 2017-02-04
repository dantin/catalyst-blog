+++
description = "Leetcode 380"
slug = "leetcode-insert-delete-getrandom-o1"
date = "2017-01-31T21:52:08+08:00"
title = "Insert Delete GetRandom O(1)"
categories = ["Code"]
tags = ["Leetcode"]
+++

### 题目

常数时间内插入删除和获得随机数。

Design a data structure that supports all following operations in average $O(1)$ time.

1. `insert(val)`: Inserts an item val to the set if not already present.
2. `remove(val)`: Removes an item val from the set if present.
3. `getRandom`: Returns a random element from current set of elements. Each element must have the __same probability__ of being returned.

__Example__:

```console
// Init an empty set.
RandomizedSet randomSet = new RandomizedSet();

// Inserts 1 to the set. Returns true as 1 was inserted successfully.
randomSet.insert(1);

// Returns false as 2 does not exist in the set.
randomSet.remove(2);

// Inserts 2 to the set, returns true. Set now contains [1,2].
randomSet.insert(2);

// getRandom should return either 1 or 2 randomly.
randomSet.getRandom();

// Removes 1 from the set, returns true. Set now contains [2].
randomSet.remove(1);

// 2 was already in the set, so return false.
randomSet.insert(2);

// Since 2 is the only number in the set, getRandom always return 2.
randomSet.getRandom();
```

### 分析

利用一个一维数组和一个哈希表，其中数组用来保存数字，哈希表用来建立每个数字和其在数组中的位置之间的映射。

对于插入操作，先看这个数字是否已经在哈希表中存在，如果存在的话直接返回false，不存在的话，将其插入到数组的末尾，然后建立数字和其位置的映射。

删除操作还是要先判断其是否在哈希表里，如果没有，直接返回false。由于哈希表的删除是常数时间的，而数组并不是，为了使数组删除也能常数级，实际上将要删除的数字和数组的最后一个数字调换个位置，然后修改对应的哈希表中的值，这样只需要删除数组的最后一个元素即可，保证了常数时间内的删除。

而返回随机数对于数组来说就很简单了，只要随机生成一个位置，返回该位置上的数字即可。

### 解法

```java
public class RandomizedSet {

    private Map<Integer, Integer> map;
    private List<Integer> nums;
    private Random random;
    private int size;

    /** Initialize your data structure here. */
    public RandomizedSet() {
        this.nums = new ArrayList<>();
        this.map = new HashMap<>();
        this.random = new Random();
        this.size = 0;
    }

    /** Inserts a value to the set. Returns true if the set did not already contain the specified element. */
    public boolean insert(int val) {
        if (map.containsKey(val)) return false;

        map.put(val, size);
        if (size == nums.size()) {
            nums.add(val);
        } else {
            nums.set(size, val);
        }
        size++;

        return true;
    }

    /** Removes a value from the set. Returns true if the set contained the specified element. */
    public boolean remove(int val) {
        if (map.isEmpty() || !map.containsKey(val)) return false;

        int idx = map.get(val);
        int last = nums.get(--size);
        nums.set(idx, last);
        map.put(last, idx);
        map.remove(val);

        return true;
    }

    /** Get a random element from the set. */
    public int getRandom() {
        int idx = random.nextInt(size);
        return nums.get(idx);
    }
}

/**
 * Your RandomizedSet object will be instantiated and called as such:
 * RandomizedSet obj = new RandomizedSet();
 * boolean param_1 = obj.insert(val);
 * boolean param_2 = obj.remove(val);
 * int param_3 = obj.getRandom();
 */
```