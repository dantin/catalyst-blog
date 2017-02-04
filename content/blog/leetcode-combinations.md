+++
date = "2017-02-01T22:49:47+08:00"
title = "Combinations"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 77"
slug = "leetcode-combinations"
+++

### 题目

求组合数。

Given two integers $n$ and $k$, return all possible combinations of $k$ numbers out of $1 \dots n$.

For example,

If $n = 4$ and $k = 2$, a solution is:

```console
[
  [2,4],
  [3,4],
  [2,3],
  [1,2],
  [1,3],
  [1,4],
]
```

### 分析

回溯法。

这道题让求1到n共n个数字里k个数的组合数的所有情况，还是要用深度优先搜索DFS来解，根据以往的经验，像这种要求出所有结果的集合，一般都是用DFS调用递归来解。

建立一个保存最终结果的大集合ans，还要定义一个保存每一个组合的小集合out，每次放一个数到out里，如果out里数个数到了k个，则把out保存到最终结果中，否则在下一层中继续调用递归。

对于n = 5, k = 3, 处理的结果如下：

```console
1   2   3 
1   2   4
1   2   5
1   3   4
1   3   5
1   4   5
2   3   4
2   3   5
2   4   5
3   4   5
```

### 解法

```java
public class Solution {
    public List<List<Integer>> combine(int n, int k) {
        List<List<Integer>> ans = new LinkedList<>();
        LinkedList<Integer> out = new LinkedList<>();
        dfs(n, k, ans, out, 1);
        return ans;
    }

    private void dfs(int n, int k, List<List<Integer>> ans, LinkedList<Integer> out, int start) {
        if (out.size() == k) {
            ans.add(new LinkedList<Integer>(out));
        } else {
            for (int i = start; i <= n; i++) {
                out.offerLast(i);
                dfs(n, k, ans, out, i + 1);
                out.pollLast();
            }
        }
    }
}
```