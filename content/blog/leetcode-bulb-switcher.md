+++
date = "2016-12-24T21:45:49+08:00"
title = "Bulb Switcher"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 319"
slug = "leetcode-bulb-switcher"
+++


Leetcode 319

### 题目

有n盏初始处于关闭状态的灯泡。首先打开所有的灯泡。然后，熄灭所有序号为2的倍数的灯泡。第三轮，切换所有序号为3的倍数的灯泡（开着的就关掉，关着的就打开）。第n轮，你只切换最后一只灯泡。计算n轮之后还有几盏灯泡亮着。

There are n bulbs that are initially off. You first turn on all the bulbs. Then, you turn off every second bulb. On the third round, you toggle every third bulb (turning on if it's off or turning off if it's on). For the _i_ th round, you toggle every _i_ bulb. For the _n_ th round, you only toggle the last bulb. Find how many bulbs are on after n rounds.

__Example__:

```
Given n = 3. 

At first, the three bulbs are [off, off, off].
After first round, the three bulbs are [on, on, on].
After second round, the three bulbs are [on, off, on].
After third round, the three bulbs are [on, off, off]. 

So you should return 1, because there is only one bulb is on.
```

### 分析

只有5个灯泡的情况，'X'表示灭，‘O’表示亮，如下所示：

```
init：    X    X    X    X    X
1st：     O    O    O    O    O
2nd：     O    X    O    X    O
3rd：     O    X    X    X    O
4th：     O    X    X    O    O
5th：     O    X    X    O    X
```

那么最后五次遍历后，只有1号和4号锁是亮的，而且很巧的是它们都是平方数。

仔细研究发现，对于第k个灯泡，只有当k有奇数个整除因子，才能改变灯泡的状态，比如当k为36时，它的因数有(1,36), (2,18), (3,12), (4,9), (6,6), (9,4), (12,3), (18,2), (36, 1)。可以看到前四个括号里成对出现的因数各不相同，括号中前面的数改变了灯泡状态，后面的数又变回去了，等于锁的状态没有发生变化，只有(6,6)，改变了一次状态，没有对应其它的状态能将其变回去了，所以锁就一直是打开状态的。

所以，问题就简化为了求1到n之间完全平方数的个数，我们可以用force brute来比较从1开始的完全平方数和n的大小。

更进一步，这个数就是n的平方根取整。

### 解法

方法一：

```java
public class Solution {
    public int bulbSwitch(int n) {
        int ans = 1;
        while (ans * ans <= n) ans++;
        return ans - 1;
    }
}
```

方法二：

```java
public class Solution {
    public int bulbSwitch(int n) {
        return (int) Math.sqrt(n);
    }
}
```
