+++
date = "2016-08-05T21:44:12+08:00"
title = "二叉树"
categories = ["Scholar"]
tags = ["Data Structure"]
description = "本文记录二叉树常见算法"
slug = "data-structure-binary-tree"
+++

### 基本概念

每个结点最多有两棵子树，左子树和右子树，次序不可以颠倒。

性质：

1. 非空二叉树的第n层上至多有`2^(n-1)`个元素。
2. 深度为h的二叉树至多有`2^h-1`个结点。

满二叉树：所有叶子节点都在同一层次，且非叶子结点的度数为2。在满二叉树中若其深度为h，则其所包含的结点数必为`2^h-1`。

完全二叉树：除了最大的层次即成为一颗满二叉树且层次最大那层所有的结点均向左靠齐，即集中在左面的位置上，不能有空位置。
对于完全二叉树，设一个结点为i则其父节点为i/2，2i为左子节点，2i+1为右子节点。

### 存储结构

* 顺序存储：存储在数组中，速度有优势，但是所占空间较大；
* 链式存储：用指针表示父子关系，主流；

代码实现

```python
class Node(object):
    
    def __init__(self, data, left, right):
        self.data = data
        self.left = left
        self.right = right
```

### 构造二叉树

输入某二叉树的前序遍历和中序遍历的结果，请重建出该二叉树。假设输入的前序遍历和中序遍历的结果中都不含重复的数字。

这道题比较容易，前序遍历的结果中，第一个结点一定是根结点，然后在中序遍历的结果中查找这个根结点，根结点左边的就是左子树，根结点右边的就是右子树，递归构造出左、右子树即可。示意图如图所示：

![构造二叉树](/images/binary-tree-create.png "Binary-tree-create")

代码实现

```python
def construct_tree(pre_order, mid_order):
    if len(pre_order) != len(mid_order):
        raise Exception('bad parameter')

    if len(pre_order) == 0:
        return None

    root_data = pre_order[0]
    for i in xrange(len(mid_order)):
        if mid_order[i] == root_data:
            break
    left = construct_tree(pre_order[1 : 1 + i], mid_order[:i])
    right = construct_tree(pre_order[1 + i:], mid_order[i + 1:])
    return Node(root_data, left, right)
```

### 遍历二叉树

遍历即将树的所有结点访问且仅访问一次。按照根节点位置的不同分为前序遍历，中序遍历，后序遍历。

* 前序遍历：根节点->左子树->右子树
* 中序遍历：左子树->根节点->右子树
* 后序遍历：左子树->右子树->根节点

代码实现

```python
def preorder(root):
    if root:
        print root.data
        preorder(root.left)
        preorder(root.right)

def midorder(root):
    if root:
        midorder(root.left)
        print root.data
        midorder(root.right)

def postorder(root):
    if root:
        postorder(root.left)
        postorder(root.right)
        print root.data
```

### 节点个数

代码实现

```python
def tree_node_count(root):
    if root:
        return tree_node_count(root.left) + tree_node_count(root.right) + 1
    else:
        return 0
```

### 树的深度

代码实现

```python
def tree_height(root):
    if not root:
        return 0
    left = tree_height(root.left)
    right = tree_height(root.right)
    return (left if left > right else right) + 1
```

参考

[CSDN](http://blog.csdn.net/fansongy/article/details/6798278)
