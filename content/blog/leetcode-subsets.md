+++
tags = ["Leetcode"]
description = "Leetcode 78"
date = "2017-02-14T23:06:32+08:00"
title = "Subsets"
slug = "leetcode-subsets"
categories = ["Code"]
+++

### 题目

给一组不同数字，求它所有可能的子集。

Given a set of __distinct__ integers, _nums_, return all possible subsets.

__Note__: The solution set must not contain duplicate subsets.

For example,

If _nums_ = $[1,2,3]$, a solution is:

```console
[
  [3],
  [1],
  [2],
  [1,2,3],
  [1,3],
  [2,3],
  [1,2],
  []
]
```

### 分析

方法一：

DFS：进入扫描时把当前subset加入集合。

方法二：

起始subset集为：$[]$

添加S0后为：$[], [S0]$

添加S1后为：$[], [S0], [S1], [S0, S1]$

添加S2后为：$[], [S0], [S1], [S0, S1], [S2], [S0, S2], [S1, S2], [S0, S1, S2]$

红色subset为每次新增的。显然规律为添加Si后，新增的subset为克隆现有的所有subset，并在它们后面都加上Si。

方法三：

由于$nums[0 : n-1]$组成的每一个subset，可以看成是对是否包含$nums[i]$的取舍。$nums[i]$只有两种状态，包含在特定subset内，或不包含。所以subset的数量总共有$2^n$个。所以可以用$0 \to 2^{n-1}$的二进制来表示一个subset。二进制中每个0/1表示该位置的$S[i]$是否包括在当前subset中。

### 解法

方法一：

```java
public class Solution {
    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> ans = new LinkedList<>();
        if (nums == null || nums.length == 0) return ans;

        List<Integer> path = new ArrayList<>();
        dfs(nums, 0, path, ans);

        return ans;
    }

    private void dfs(int[] nums, int from, List<Integer> path, List<List<Integer>> subsets) {
        subsets.add(new ArrayList<Integer>(path));
        for (int i = from; i < nums.length; i++) {
            path.add(nums[i]);
            dfs(nums, i + 1, path, subsets);
            path.remove(path.size() - 1);
        }
    }
}
```

方法二：

```java
public class Solution {
    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> ans = new LinkedList<>();
        if (nums == null || nums.length == 0) return ans;

        ans.add(new ArrayList<Integer>());
        for (int i = 0; i < nums.length; i++) {
            int n = ans.size();
            for (int j = 0; j < n; j++) {
                List<Integer> subset = new ArrayList<Integer>(ans.get(j));
                subset.add(nums[i]);
                ans.add(new ArrayList<Integer>(subset));
            }
        }

        return ans;
    }
}
```

方法三：

```java
public class Solution {
    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> ans = new LinkedList<>();
        int max = 1;
        for (int i = 0; i < nums.length; i++) {
            max <<= 1;
        }
        for (int i = 0; i < max; i++) {
            ans.add(num2set(nums, i));
        }
        return ans;
    }

    private List<Integer> num2set(int[] nums, int num) {
        List<Integer> set = new ArrayList<>();
        int i = 0;
        while (num > 0) {
            if ((num & 1) == 1) set.add(nums[i]);
            num >>>= 1;
            i++;
        }
        return set;
    }

}
```
