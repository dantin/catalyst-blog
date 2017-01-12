+++
date = "2016-12-25T22:13:43+08:00"
title = "Reconstruct Original Digits from English"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 423"
slug = "leetcode-reconstruct-original-digits-from-english"
+++

### 题目

从英文字母重建数字。

Given a __non-empty__ string containing an out-of-order English representation of digits `0-9`, output the digits in ascending order.

__Note__:

1. Input contains only lowercase English letters.
2. Input is guaranteed to be valid and can be transformed to its original digits. That means invalid inputs such as "abc" or "zerone" are not permitted.
3. Input length is less than 50,000.

__Example 1__:

```console
Input: "owoztneoer"

Output: "012"
```

__Example 2__:

```console
Input: "fviefuro"

Output: "45"
```

### 分析

穷举算法。

首先统计各个字符出现的次数，然后算出每个单词出现的次数，就可以重建了。

由于题目中限定了输入的字符串一定是有效的，那么不会出现无法成功重建的情况。

仔细观察这些表示数字的单词"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"，可以发现有些的单词的字符是独一无二的，比如z，只出现在zero中，还有w，u，x，g这四个单词，分别只出现在two，four，six，eight中，那么这五个数字的个数就可以被确定了，由于含有o的单词有zero，two，four，one，其中前三个都被确定了，那么one的个数也就知道了；由于含有h的单词有eight，three，其中eight个数已知，那么three的个数就知道了；由于含有f的单词有four，five，其中four个数已知，那么five的个数就知道了；由于含有s的单词有six，seven，其中six个数已知，那么seven的个数就知道了；由于含有i的单词有six，eight，five，nine，其中前三个都被确定了，那么nine的个数就知道了，按这个顺序"zero", "two", "four", "six", "eight", "one", "three", "five", "seven", "nine"就能找出所有的个数了。

### 解法

```java
public class Solution {
    public String originalDigits(String s) {
        int[] cache = new int[128];
        for (char c : s.toCharArray()) {
            cache[c]++;
        }
        int[] nums = new int[10];
        nums[0] = cache['z'];
        nums[2] = cache['w'];
        nums[4] = cache['u'];
        nums[6] = cache['x'];
        nums[8] = cache['g'];
        nums[1] = cache['o'] - nums[0] - nums[2] - nums[4];
        nums[3] = cache['h'] - nums[8];
        nums[5] = cache['f'] - nums[4];
        nums[7] = cache['s'] - nums[6];
        nums[9] = cache['i'] - nums[6] - nums[8] - nums[5];

        StringBuilder ans = new StringBuilder();
        for (int i = 0; i < nums.length; i++) {
            for (int j = 0; j < nums[i]; j++) {
                ans.append(i);
            }
        }

        return ans.toString();
    }
}
```