---
title: Find All Anagrams in a String
date: 2016-11-11 17:08:45
categories: 学术
tags: Leetcode
toc: true
---

Leetcode 438

### 题目

查找字符串中的所有Anagrams，即：排列顺序不同的字符串。

Given a string s and a __non-empty__ string __p__, find all the start indices of __p__'s anagrams in __s__.

Strings consists of lowercase English letters only and the length of both strings __s__ and __p__ will not be larger than 20,100.

The order of output does not matter.

__Example 1__:

```
Input:
s: "cbaebabacd" p: "abc"

Output:
[0, 6]

Explanation:
The substring with start index = 0 is "cba", which is an anagram of "abc".
The substring with start index = 6 is "bac", which is an anagram of "abc".
```

__Example 2__:

```
Input:
s: "abab" p: "ab"

Output:
[0, 1, 2]

Explanation:
The substring with start index = 0 is "ab", which is an anagram of "ab".
The substring with start index = 1 is "ba", which is an anagram of "ab".
The substring with start index = 2 is "ab", which is an anagram of "ab".
```

### 分析

基本思路是用一个窗口，取窗口中的数据指纹和Anagram做匹配，如果相同，则输出。

### 解法

解法一：

思路比较简单，先找出Anagram模式；对于每一个节点，往前退Anagram长度的步数做匹配。

```java
public class Solution {
    public List<Integer> findAnagrams(String s, String p) {
        List<Integer> locations = new ArrayList<>();

        int[] characters = new int[26];
        for(int i = 0; i < p.length(); i++) {
            char c = p.charAt(i);
            characters[c - 'a']++;
        }

        for(int i = 0; i < s.length(); i++) {
            int[] current = new int[26];
            System.arraycopy(characters, 0, current, 0, 26);

            for(int j = i + p.length() - 1; j < s.length() && j >= i; j--) {
                char c = s.charAt(j);
                if(characters[c - 'a'] > 0) {
                    if(current[c - 'a'] > 0) current[c - 'a']--;
                } else {
                    break;
                }
            }

            int remaining = 0;
            for(int k = 0; k < current.length; k++) {
                remaining += current[k];
            }
            if(remaining == 0) locations.add(i);
        }
        return locations;
    }
}
```

解法二：

固定一个窗口，初始窗口只是增加，当窗口长度达到Anagram时，则一进一出。同时比较窗口中的Anagram模式。

```java
public class Solution {
    public List<Integer> findAnagrams(String s, String p) {
        List<Integer> locations = new ArrayList<>();

        int[] characters = new int[128];
        for(int i = 0; i < p.length(); i++) {
            characters[p.charAt(i)]++;
        }

        int[] window = new int[128];
        for(int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            window[c]++;
            if(i >= p.length()) {
                char oc = s.charAt(i - p.length());
                window[oc]--;
            }
            if(Arrays.equals(characters, window)) {
                locations.add(i + 1 - p.length());
            }
        }

        return locations;
    }
}
```

解法三：下面的代码将时间复杂度优化至O(n)

字典cp记录要凑成目标字符串p的anagram，各字符分别缺多少个

整数count记录凑成目标字符串p一共还缺多少个字符

参考[LeetCode Discuss](https://discuss.leetcode.com/topic/64434/shortest-concise-java-o-n-sliding-window-solution)

```java
public class Solution {
    public List<Integer> findAnagrams(String s, String p) {
        List<Integer> locations = new ArrayList<>();

        int[] hash = new int[256];
        for(char c : p.toCharArray()) {
            hash[c]++;
        }

        int left = 0, right = 0, count = p.length();
        while(right < s.length()) {
            if(hash[s.charAt(right++)]-- >= 1) count--;
            if(count == 0) locations.add(left);
            if(right - left == p.length() && hash[s.charAt(left++)]++ >= 0) count++;
        }

        return locations;
    }
}
```
