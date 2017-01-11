+++
date = "2017-01-01T14:36:17+08:00"
title = "Maximum XOR of Two Numbers in an Array"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 421"
slug = "leetcode-maximum-xor-of-two-numbers-in-an-array"
+++

### 题目

求数组中两个数字异或的最大值。

Given a __non-empty__ array of numbers, 

$$
\begin{aligned}
a\_0, a\_1, a\_2, \dots, a\_{n-1}
\end{aligned}
$$

where $0 \le a_i < 2^{31}$.

Find the maximum result of $a_i XOR a_j$, where $0 \le i, j < n$.

Could you do this in O(n) runtime?

__Example__:

```console
Input: [3, 10, 5, 25, 2, 8]

Output: 28

Explanation: The maximum result is 5 ^ 25 = 28.
```

### 分析

利用XOR的性质，$a \oplus b = c$，则有$a \oplus c = b$，且$b \oplus c = a$。

每次从高位开始，到某一位为止，所能获得的最大的数。设置变量mask用来表示能形成的值，每一次将mask和其他的num相与得到的值加入set，表示在当前这一位上，数组里有这么多prefix。

假定在某一位上的任意两数xor能得到的最大值是tmp,那么他一定满足a(xor)b = tmp,其中set.contains(a) && set.contains(b). 所以，我们只需要判断b(xor)tmp的结果是不是在当前这一位下的set内，就可以知道这个tmp能不能又这个set中的任意两个数组成。


### 解法

```java
public class Solution {
    public int findMaximumXOR(int[] nums) {
        int max = 0, mask = 0;
        for (int i = 31; i >= 0; i--) {
            mask |= (1 << i);
            Set<Integer> set = new HashSet<>();
            for (int num : nums) {
                set.add(num & mask);
            }
            int tmp = max | (1 << i);
            for (Integer prefix : set) {
                if (set.contains(prefix ^ tmp)) {
                    max = tmp;
                    break;
                }
            }
        }
        return max;
    }
}
```
