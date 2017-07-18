+++
description = "Leetcode 500"
slug = "leetcode-keyboard-row"
date = "2017-06-08T12:03:24+08:00"
title = "Keyboard Row"
categories = ["Code"]
tags = ["Leetcode"]
+++

### 题目

判断单词中的字符是否为键盘中的一行。

Given a List of words, return the words that can be typed using letters of __alphabet__ on only one row's of American keyboard like the image below.

__Example 1__:

```console
Input: ["Hello", "Alaska", "Dad", "Peace"]
Output: ["Alaska", "Dad"]
```

__Note__:

1. You may use one character in the keyboard more than once.
2. You may assume the input string will only contain letters of alphabet.

### 分析

构造Map，遍历单词中的字符进行判断。

### 解法

```go
func findWords(words []string) []string {
    keybord := [][]rune{
        []rune{'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'},
        []rune{'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'},
        []rune{'z', 'x', 'c', 'v', 'b', 'n', 'm'},
    }
    char_map := make(map[rune]int)
    for row, chars := range keybord {
        for _, c := range chars {
            char_map[c] = row
            char_map[unicode.ToUpper(c)] = row
        }
    }

    res := make([]string, 0)
    for _, word := range words {
        cs := []rune(word)
        row := char_map[cs[0]]
        f := true
        for _, c := range cs {
            if char_map[c] != row {
                f = false
                break;
            }
        }
        if f {
            res = append(res, word)
        }
    }

    return res
}
```
