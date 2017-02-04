+++
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 390"
date = "2017-01-28T22:07:31+08:00"
title = "Elimination Game"
slug = "leetcode-elimination-game"
+++

### 题目

给定一个数字1到n组成的有序列表。从左边的第一个数字开始向右，每隔一位移除一个数字，直到列表末尾。

重复上面的步骤，但是这一次从右向左，移除最右侧的数字，然后从剩余的数字中每隔一位移除一个数字。

重复执行上述过程，从左到右、从右到左进行切换，直到只剩下一个数字为止。

寻找最后一个剩下的数字。

There is a list of sorted integers from 1 to n. Starting from left to right, remove the first number and every other number afterward until you reach the end of the list.

Repeat the previous step again, but this time from right to left, remove the right most number and every other number from the remaining numbers.

We keep repeating the steps again, alternating left to right and right to left, until a single number remains.

Find the last number that remains starting with a list of length n.

__Example__:

```console
Input:
n = 9,
1 2 3 4 5 6 7 8 9
2 4 6 8
2 6
6

Output:
6
```

### 分析

两个简单的例子：

当$n = 8$时：

第一轮：$\underline{1} 2 \underline{3} 4 \underline{5} 6 \underline{7} 8$

第二轮：$2 \underline{4} 6 \underline{8}$

第三轮：$\underline{2} 6$

最终结果：$6$

当$n = 7$时：

第一轮：$\underline{1} 2 \underline{3} 4 \underline{5} 6 \underline{7}$

第二轮：$\underline{2} 4 \underline{6}$

最终结果：$4$

从左往右删的时候，每次都是删掉第一个数字，而从右往左删的时候，则有可能删掉第一个或者第二个数字，而且每删一次，数字之间的距离会变为之前的两倍。

要做的是每次记录当前数组的第一个数字，而且通过观察可以看出，从右往左删时，如果剩下的数字个数是偶数个时，删掉的是第二个数字；如果是奇数个的时候，删掉的是第一个数字。

总结出了上述规律，就可以写出代码如下：

### 解法

```java
public class Solution {
    public int lastRemaining(int n) {
        int base = 1, ans = 1;
        while (base * 2 <= n) {
            ans += base;
            base *= 2;
            if (base * 2 > n) break;
            if ((n / base) % 2 == 1) ans += base;
            base *= 2;
        }
        return ans;
    }
}
```
