+++
date = "2016-12-19T22:45:03+08:00"
title = "Maximum Product of Word Lengths"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 318"
slug = "leetcode-maximum-product-of-word-lengths"
+++


Leetcode 318

### 题目

求两个没有相同字母的单词的长度之积的最大值。

Given a string array words, find the maximum value of length(word[i]) * length(word[j]) where the two words do not share common letters. You may assume that each word will contain only lower case letters. If no such two words exist, return 0.

__Example 1__:

```
Given ["abcw", "baz", "foo", "bar", "xtfn", "abcdef"]
Return 16
The two words can be "abcw", "xtfn".
```

__Example 2__:

```
Given ["a", "ab", "abc", "d", "cd", "bcd", "abcd"]
Return 4
The two words can be "ab", "cd".
```

__Example 3__:

```
Given ["a", "aa", "aaa", "aaaa"]
Return 0
No such pair of words.
```

### 分析

最初的想法是通过HashSet比较两个字符串是否有相同字符，若无，则计算两个单词长度之积，并更新结果。这种做法超时。

优化做法：

用mask，因为题目中说都是小写字母，那么只有26位，一个整型数int有32位，我们可以用后26位来对应26个字母，若为1，说明该对应位置的字母出现过，那么每个单词的都可由一个int数字表示。

两个单词没有共同字母的条件是这两个int数AND结果为0，用这个判断方法即可。

### 解法

```java
public class Solution {
    public int maxProduct(String[] words) {
        int ans = 0;
        int[] mask = new int[words.length];
        for(int i = 0; i < words.length; i++) {
            for(char c : words[i].toCharArray()) {
                mask[i] |= 1 << (c - 'a');
            }
            for(int j = 0; j < i; j++) {
                if((mask[i] & mask[j]) == 0) {
                    ans = Math.max(ans, words[i].length() * words[j].length());
                }
            }
        }
        return ans;
    }
}
```

参考：

[Leetcode Discuss](https://leetcode.com/discuss/74580/bit-shorter-c)
