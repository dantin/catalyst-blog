+++
date = "2017-01-09T13:59:40+08:00"
title = "Longest Repeating Character Replacement"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 424"
slug = "leetcode-longest-repeating-character-replacement"
+++

### 题目

最长重复字符置换。

Given a string that consists of only uppercase English letters, you can replace any letter in the string with another letter at most _k_ times. Find the length of a longest substring containing all repeating letters you can get after performing the above operations.

__Note__:

Both the string's length and k will not exceed 104.

__Example 1__:

```console
Input:
s = "ABAB", k = 2

Output:
4

Explanation:
Replace the two 'A's with two 'B's or vice versa.
```

__Example 2__:

```console
Input:
s = "AABABBA", k = 1

Output:
4

Explanation:
Replace the one 'A' in the middle with 'B' and form "AABBBBA".
The substring "BBBB" has the longest repeating letters, which is 4.
```

### 分析

使用滑动窗口(Sliding Window)算法。

如果没有k的限制，即把字符串变成只有一个字符重复的字符串需要的最小置换次数，那么就是字符串的总长度减去出现次数最多的字符的个数。

如果加上k的限制，其实就是求满足$(\text{子字符串的长度} - \text{出现次数最多的字符个数}) \le k$的最大子字符串长度即可

用一个变量slow记录滑动窗口左边界，初始化为0，然后我们遍历字符串，每次累加出现字符的个数，然后更新出现最多字符的个数，判断当前滑动窗口是否满足之前说的那个条件，如果不满足，我们就把滑动窗口左边界向右移动一个，并注意去掉的字符要在counts里减一，直到满足条件，我们更新结果ans即可。

### 解法

利用全部是大小写字母

```java
public class LongestRepeatingCharacterReplacement {
    public int characterReplacement(String s, int k) {
        int ans = 0, max = 0, slow = 0;
        int[] counts = new int[128];
        for (int fast = 0; fast < s.length(); fast++) {
            max = Math.max(max, ++counts[s.charAt(fast)]);
            while (fast - slow + 1 - max > k) {
                counts[s.charAt(slow)]--;
                slow++;
            }
            ans = Math.max(ans, fast - slow + 1);
        }
        return ans;
    }

    public static void main(String[] args) {
        String s = "ABAB";
        int k = 2;

        System.out.printf("s = %s\n", s);
        System.out.printf("k = %d\n", k);
        LongestRepeatingCharacterReplacement solution = new LongestRepeatingCharacterReplacement();
        System.out.println(solution.characterReplacement(s, k));
    }
}
```