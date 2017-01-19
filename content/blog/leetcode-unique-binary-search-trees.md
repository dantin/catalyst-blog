+++
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 96"
slug = "leetcode-unique-binary-search-trees"
date = "2017-01-18T07:04:43+08:00"
title = "Unique Binary Search Trees"
+++

### 题目

给定一个数字n，给出$[1, 2, \dots, n]$能够构造的不同BST的个数。

Given $n$, how many structurally unique BST's (binary search trees) that store values $1 \dots n$?

For example,

Given $n = 3$, there are a total of $5$ unique BST's.

```console
 1         3     3      2      1
  \       /     /      / \      \
   3     2     1      1   3      2
  /     /       \                 \
 2     1         2                 3
```

### 分析

找规律，这里是BST，因此数字会对插入的位置有影响。

当$n = 1$时

```console
1
```

当$n = 2$时

```console
 1      2
  \    /
   2  1
```

当$n = 3$时

```console
 1    1          3     3      2
  \    \        /     /      / \
   3    2      2     1      1   3
  /      \    /       \
 2        3  1         2
```

定义$f(n)$为unique BST的数量。

以$n = 3$为例：

构造的BST的根节点可以取${1, 2, 3}$中的任一数字。

* 如果以1为节点，则左子树只能有0个节点，而右子树有2, 3两个节点，则left/right subtree一共的combination数量为：$f(0) \cdot f(2) = 1 \times 2 = 2$
* 以2为节点，则左子树只能为1，右子树只能为2：$f(1) \cdot f(1) = 1 \times 1 = 1$
* 以3为节点，则左子树有1, 2两个节点，右子树有0个节点：$f(2) \cdot f(0) = 2 \times 1 = 2$

__递推公式__

$f(0) = 1$

$f(n) = \sum_{i=0}^{n-1} f(i) \cdot f(n-i-1)$

### 解法

```java
public class Solution {
    public int numTrees(int n) {
        int[] dp = new int[n + 1];
        dp[0] = 1;

        for (int i = 0; i < dp.length; i++) {
            for (int j = 0; j < i; j++) {
                dp[i] += dp[j] * dp[i - j - 1];
            }
        }
        return dp[n];
    }
}
```