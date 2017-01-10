+++
date = "2016-12-18T22:49:04+08:00"
title = "Assign Cookies"
categories = ["Code"]
tags = ["Leetcode"]
description = "Leetcode 455"
slug = "leetcode-assign-cookies"
+++


Leetcode 455

### 题目

有一堆cookie，每个cookie的大小不同，还有一堆小朋友，每个小朋友的胃口也不同的，问当前的cookie最多能满足几个小朋友。

Assume you are an awesome parent and want to give your children some cookies. But, you should give each child at most one cookie. Each child i has a greed factor gi, which is the minimum size of a cookie that the child will be content with; and each cookie j has a size sj. If sj >= gi, we can assign the cookie j to the child i, and the child i will be content. Your goal is to maximize the number of your content children and output the maximum number.

__Note__:

You may assume the greed factor is always positive. 

You cannot assign more than one cookie to one child.

__Example 1__:

```
Input: [1,2,3], [1,1]

Output: 1

Explanation: You have 3 children and 2 cookies. The greed factors of 3 children are 1, 2, 3. 
And even though you have 2 cookies, since their size is both 1, you could only make the child whose greed factor is 1 content.
You need to output 1.
```

__Example 2__:

```
Input: [1,2], [1,2,3]

Output: 2

Explanation: You have 2 children and 3 cookies. The greed factors of 2 children are 1, 2. 
You have 3 cookies and their sizes are big enough to gratify all of the children, 
You need to output 2.
```

### 分析

典型的贪婪算法，先对两个数组进行排序，让小的在前面。然后拿最小的cookie给胃口最小的小朋友，看能否满足，能的话，我们结果res自加1，然后再拿下一个cookie去满足下一位小朋友；如果当前cookie不能满足当前小朋友，那么我们就用下一块稍大一点的cookie去尝试满足当前的小朋友。当cookie发完了或者小朋友没有了就停止遍历。

### 解法

```java
public class Solution {
    public int findContentChildren(int[] g, int[] s) {
        Arrays.sort(g);
        Arrays.sort(s);

        int p = 0;
        int count = 0;
        for(int i = 0; i < s.length; i++) {
            if(s[i] >= g[p]) {
                count++;
                p++;
                if(p >= g.length) break;
            }
        }

        return count;
    }
}
```