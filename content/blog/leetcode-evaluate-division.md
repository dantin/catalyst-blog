+++
tags = ["Leetcode"]
description = "Leetcode 399"
slug = "leetcode-evaluate-division"
categories = ["Code"]
date = "2017-01-16T10:59:41+08:00"
title = "Evaluate Division"
+++

### 题目

求除法表达式的值。

Equations are given in the format $A / B = k$, where $A$ and $B$ are variables represented as strings, and $k$ is a real number (floating point number). Given some queries, return the answers. If the answer does not exist, return $-1.0$.

__Example__:

Given $a / b = 2.0, b / c = 3.0$.

queries are: $a / c = ?, b / a = ?, a / e = ?, a / a = ?, x / x = ?$.

return $[6.0, 0.5, -1.0, 1.0, -1.0 ]$.

The input is: `vector<pair<string, string>> equations, vector<double>& values, vector<pair<string, string>> queries`, where `equations.size() == values.size()`, and the values are positive. This represents the equations. Return `vector<double>`.

According to the example above:

```console
equations = [ ["a", "b"], ["b", "c"] ],
values = [2.0, 3.0],
queries = [ ["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"] ]. 
The input is always valid. You may assume that evaluating the queries will result in no division by zero and there is no contradiction.
```

### 分析

分情况讨论：

如果需要分析的除法式的除数和被除数如果其中任意一个没有在已知条件中出现过，那么返回结果-1。

不能直接由已知条件得到的情况主要有下面三种：

1. 已知: $a / b = 2, b / c = 3$， 求$a / c$
2. 已知: $a / c = 2, b / c = 3$， 求$a / b$
3. 已知: $a / b = 2, a / c = 3$， 求$b / c$

在递归函数中，需要分析的除法表达式，遍历所有的已知条件，如果跟某一个已知表达式相等，直接返回结果，或者跟某一个已知表达式正好相反，那么返回已知表达式结果的倒数即可。

如果都没有的话，那么就需要间接寻找了，需要一个stack来记录已经访问过的表达式，先看待求表达式的被除数和当前遍历到的已知表达式的被除数是否相同如果相同，那么就是上面的第一种情况，可以把待求表达式的被输出换成已知表达式的除数，比如要求$a/c$就换成了求$b/c$，而求$b/c$的过程就可以调用递归函数来求解（结果要乘以$a/b$的值）。

如果算出来是正数则直接返回，如果是非正数说明没有找到。

对于上面的第一种情况，如果要求$c/a$，那么上面的方法就没法开始查找，所以同时也要看待求表达式的除数和当前遍历到的已知表达式的被除数是否相同，后面的处理方法都相同。

### 解法

```java
public class Solution {
    public double[] calcEquation(String[][] equations, double[] values, String[][] queries) {
        double[] ans = new double[queries.length];
        // filter unexcepted words
        Set<String> set = new HashSet<>();
        for (String[] equation : equations) {
            set.add(equation[0]);
            set.add(equation[1]);
        }

        for (int i = 0; i < queries.length; i++) {
            String[] tokens = queries[i];
            if (!set.contains(tokens[0]) || !set.contains(tokens[1])) {
                ans[i] = -1D;
            } else {
                Deque<Integer> stack = new LinkedList<>();
                ans[i] = evaluate(equations, values, tokens, stack);
            }

        }

        return ans;
    }
    
    private double evaluate(String[][] equations, double[] values, String[] tokens, Deque<Integer> stack) {
        // directly lookup
        for (int i = 0; i < equations.length; i++) {
            if (equations[i][0].equals(tokens[0]) && equations[i][1].equals(tokens[1])) return values[i];
            if (equations[i][0].equals(tokens[1]) && equations[i][1].equals(tokens[0])) return 1 / values[i];
        }
        // indirectly lookup
        for (int i = 0; i < equations.length; i++) {
            if (!stack.contains(i) && tokens[0].equals(equations[i][0])) {
                stack.push(i);
                double temp = values[i] * evaluate(equations, values, new String[] {equations[i][1], tokens[1]}, stack);
                if (temp > 0) {
                    return temp;
                } else {
                    stack.pop();
                }
            }
            if (!stack.contains(i) && tokens[0].equals(equations[i][1])) {
                stack.push(i);
                double temp = evaluate(equations, values, new String[] {equations[i][0], tokens[1]}, stack) / values[i];
                if (temp > 0) {
                    return temp;
                } else {
                    stack.pop();
                }
            }
        }
        return -1D;
    }
}
```

参考：

* [Leetcode Discuss](https://discuss.leetcode.com/topic/58355/esay-understand-java-solution-3ms)