+++
date = "2017-01-08T14:01:58+08:00"
title = "Decode String"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 394"
slug = "leetcode-decode-string"
+++

### 题目

解码字符串。

Given an encoded string, return it's decoded string.

The encoding rule is: $k[\text{encoded_string}]$, where the *encoded_string* inside the square brackets is being repeated exactly _k_ times. Note that _k_ is guaranteed to be a positive integer.

You may assume that the input string is always valid; No extra white spaces, square brackets are well-formed, etc.

Furthermore, you may assume that the original data does not contain any digits and that digits are only for those repeat numbers, k. For example, there won't be input like $3a$ or $2[4]$.

__Examples__:

```console
s = "3[a]2[bc]", return "aaabcbc".
s = "3[a2[c]]", return "accaccacc".
s = "2[abc]3[cd]ef", return "abcabccdcdcdef".
```

### 分析

迭代算法，需要用stack来辅助运算。

这里用两个stack，一个用来保存个数，一个用来保存字符串，遍历输入字符串，如果遇到数字，更新计数变量cnt；如果遇到左中括号，把当前cnt压入数字栈中，把当前t压入字符串栈中；如果遇到右中括号时，取出数字栈中顶元素，存入变量k，然后给字符串栈的顶元素循环加上k个t字符串，然后取出顶元素存入字符串t中；如果遇到字母，直接加入字符串t中即可。

### 解法

```java
public class Solution {
    public String decodeString(String s) {
        StringBuilder tmp = new StringBuilder();

        Deque<Integer> digits = new LinkedList<>();
        Deque<StringBuilder> tokens = new LinkedList<>();
        int cnt = 0;

        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (Character.isDigit(ch)) {
                cnt *= 10;
                cnt += ch - '0';
            } else if (ch == '[') {
                digits.push(cnt);
                tokens.push(new StringBuilder(tmp));
                cnt = 0;
                tmp.setLength(0);
            } else if (ch == ']') {
                int k = digits.pop();
                while (k-- > 0) {
                    tokens.peek().append(tmp);
                }
                tmp = tokens.pop();
            } else {
                tmp.append(ch);
            }
        }

        return tokens.isEmpty() ? tmp.toString() : tokens.pop().toString();
    }
}
```