+++
date = "2017-06-01T18:55:47+08:00"
title = "Reverse Words in a String III"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 557"
slug = "leetcode-reverse-words-in-a-string-iii"
+++

### 题目

反转字符串中的单词。

Given a string, you need to reverse the order of characters in each word within a sentence while still preserving whitespace and initial word order.

__Example 1__:

```console
Input: "Let's take LeetCode contest"
Output: "s'teL ekat edoCteeL tsetnoc"
```

__Note__: In the string, each word is separated by single space and there will not be any extra space in the string.

### 分析

用空格分隔每个单词，单词内部互换字符，注意边界条件。

### 解法

```go
func reverseWords(s string) string {
    buf := []rune(s)

    for i := 0; i < len(buf); i++ {
        if buf[i] != ' ' {
            j := i
            for j < len(buf) && buf[j] != ' ' {
                j++
            }
            reverse(buf, i, j-1)
            i = j
        }
    }

    return string(buf)
}

func reverse(s []rune, i int, j int) {
    for ; i < j; i, j = i+1, j-1 {
        s[i], s[j] = s[j], s[i]
    }
}
```
