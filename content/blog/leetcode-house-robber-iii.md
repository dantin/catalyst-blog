+++
date = "2017-01-04T09:53:24+08:00"
title = "House Robber III"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 337"
slug = "leetcode-house-robber-iii"
+++


Leetcode 337

### 题目

升级2.0版的[House Robber](/2016/11/04/leetcode-house-robber/)，沿着二叉树开始偷，求最大可能的抢劫数量，不能相邻取。

The thief has found himself a new place for his thievery again. There is only one entrance to this area, called the "root." Besides the root, each house has one and only one parent house. After a tour, the smart thief realized that "all houses in this place forms a binary tree". It will automatically contact the police if two directly-linked houses were broken into on the same night.

Determine the maximum amount of money the thief can rob tonight without alerting the police.

__Example 1__:

```
     3
    / \
   2   3
    \   \ 
     3   1
```

Maximum amount of money the thief can rob = 3 + 3 + 1 = 7.

__Example 2__:

```
     3
    / \
   4   5
  / \   \ 
 1   3   1
```

Maximum amount of money the thief can rob = 4 + 5 = 9.

### 分析

利用回溯法来做。

当前的计算需要依赖之前的结果，对于某一个节点，如果其左子节点存在，我们通过递归调用函数，算出不包含左子节点返回的值，同理，如果右子节点存在，算出不包含右子节点返回的值。

每个节点的最大值可能有两种情况：

1. 该节点值加上不包含左子节点和右子节点的返回值之和；
2. 左右子节点返回值之和不包含当期节点值；

取两者的较大值返回即可。

### 解法

```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
public class Solution {
    public int rob(TreeNode root) {
        if (root == null) return 0;
        int val = 0;
        if (root.left != null) {
            val += rob(root.left.left) + rob(root.left.right);
        }
        if (root.right != null) {
            val += rob(root.right.left) + rob(root.right.right);
        }

        return Math.max(root.val + val, rob(root.left) + rob(root.right));
    }
}
```

加缓存，提升性能：

```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
public class Solution {
    public int rob(TreeNode root) {
        Map<TreeNode, Integer> cache = new HashMap<>();
        return dfs(root, cache);
    }

    private int dfs(TreeNode root, Map<TreeNode, Integer> cache) {
        if (root == null) return 0;
        if (cache.containsKey(root)) return cache.get(root);
        int val = 0;
        if (root.left != null) {
            val += dfs(root.left.left, cache) + dfs(root.left.right, cache);
        }
        if (root.right != null) {
            val += dfs(root.right.left, cache) + dfs(root.right.right, cache);
        }

        val = Math.max(root.val + val, dfs(root.left, cache) + dfs(root.right, cache));
        cache.put(root, val);
        return val;
    }
}
```