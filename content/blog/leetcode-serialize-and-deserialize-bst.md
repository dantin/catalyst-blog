+++
date = "2016-12-29T23:11:16+08:00"
title = "Serialize and Deserialize BST"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 449"
slug = "leetcode-serialize-and-deserialize-bst"
+++


Leetcode 449

### 题目

序列化/反序列化一棵二叉搜索树。

Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.

Design an algorithm to serialize and deserialize a __binary search tree__. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary search tree can be serialized to a string and this string can be deserialized to the original tree structure.

__The encoded string should be as compact as possible.__

__Note__: Do not use class member/global/static variables to store states. Your serialize and deserialize algorithms should be stateless.

### 分析

先序遍历（Preorder Traversal）

根据二叉搜索树（BST）的性质，`左孩子 < 根节点 < 右孩子`。

可以通过先序遍历的结果唯一确定一棵原始二叉树。

__序列化（Serialization）__：

```
先序遍历原始二叉树，输出逗号分隔值字符串。
```

__反序列化（Deserialization）：

利用栈（Stack）

* 节点栈nstack保存重建二叉树过程中的节点；
* 右子树栈rstack保存当前节点的右子树允许的最大值。

```

遍历序列化串：
    取当前数值为val，新增树节点node = TreeNode(val)；
    记ntop为nstack的栈顶元素；

    若val < ntop，则val为ntop的左孩子：
        ntop.left = node
        并将node压入nstack；
        将ntop.val压入rstack；
    否则，val应为右孩子，但其父节点并不一定为ntop：
        记rstack的栈顶元素为rtop，当val > rtop时，执行循环：
            如果ntop不是右孩子
                重复弹出nstack，直到ntop不是右孩子为止（nstack[0] > nstack[1]条件不成立）
            再次弹出nstack， 并弹出rstack
        上述过程执行完毕后，令ntop.right = node，并将node压入nstack
```

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
public class Codec {

    // Encodes a tree to a single string.
    public String serialize(TreeNode root) {
        List<Integer> order = new LinkedList<>();
        preOrder(root, order);
        StringBuilder buf = new StringBuilder();
        Iterator<Integer> iter = order.iterator();
        while (iter.hasNext()) {
            buf.append(iter.next());
            if (iter.hasNext()) buf.append(",");
        }
        return buf.toString();
    }
    
    private void preOrder(TreeNode root, List<Integer> order) {
        if (root == null) return;
        order.add(root.val);
        preOrder(root.left, order);
        preOrder(root.right, order);
    }

    // Decodes your encoded data to tree.
    public TreeNode deserialize(String data) {
        if (data == null || data.isEmpty()) return null;

        LinkedList<TreeNode> nstack = new LinkedList<>();
        Deque<Integer> rstack = new LinkedList<>();
        rstack.add(Integer.MAX_VALUE);
        for (String s : data.split(",")) {
            int val = Integer.parseInt(s);
            TreeNode node = new TreeNode(val);

            if (!nstack.isEmpty()) {
                TreeNode ntop = nstack.peek();
                if (val < ntop.val) {
                    ntop.left = node;
                    rstack.push(ntop.val);
                } else {
                    while (val > rstack.peek()) {
                        while (nstack.get(0).val > nstack.get(1).val) {
                            nstack.pop();
                        }
                        rstack.pop();
                        nstack.pop();
                    }
                    nstack.peek().right = node;
                }
            }
            nstack.push(node);
        }

        return nstack.peekLast();
    }
}

// Your Codec object will be instantiated and called as such:
// Codec codec = new Codec();
// codec.deserialize(codec.serialize(root));
```