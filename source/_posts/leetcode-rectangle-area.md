---
title: Rectangle Area
date: 2016-11-18 22:31:09
categories: 练习
tags: Leetcode
toc: true
---

Leetcode 223

### 题目

两个矩形的覆盖面积。

Find the total area covered by two rectilinear rectangles in a 2D plane.

Each rectangle is defined by its bottom left corner and top right corner as shown in the figure.

![Rectangle Area](/images/leetcode_rectangle_area.png "Rectangle Area")

Assume that the total area is never beyond the maximum possible value of int.

### 分析

题目可以转化为计算矩形相交部分的面积

```
S(M) = (C - A) * (D - B)
S(N) = (G - E) * (H - F)
S(M ∩ N) = max(min(C, G) - max(A, E), 0) * max(min(D, H) - max(B, F), 0)
```

### 解法

```java
import java.util.Arrays;

public class RectangleArea {

    public int computeArea(int A, int B, int C, int D, int E, int F, int G, int H) {
        int area1 = (C - A) * (D - B);
        int area2 = (G - E) * (H - F);

        int a = Math.min(C, G) - Math.max(A, E);
        int b = Math.min(D, H) - Math.max(B, F);

        System.out.println(-1500000000-1500000000);
        System.out.println(-1500000000L-1500000000L);
        System.out.printf("a: " + a + ", b: " + b);
        int intersection = Math.max(a, 0) * Math.max(b, 0);
        return area1 + area2 - intersection;
    }

    public static void main(String[] args) {
        int A = -1500000001;
        int B = 0;
        int C = -1500000000;
        int D = 1;
        int E = 1500000000;
        int F = 0;
        int G = 1500000001;
        int H = 1;

        RectangleArea solution = new RectangleArea();
        System.out.printf("Rectangle I: bottom left (%d, %d), top right (%d, %d)\n", A, B, C, D);
        System.out.printf("Rectangle II: bottom left (%d, %d), top right (%d, %d)\n", E, F, G, H);
        System.out.printf("Total Area: %d\n", solution.computeArea(A, B, C, D, E, F, G, H));
    }
}
```

在极端情况可能会溢出，如上例所示。输出为：

```bash
Rectangle I: bottom left (-1500000001, 0), top right (-1500000000, 1)
Rectangle II: bottom left (1500000000, 0), top right (1500000001, 1)
1294967296
-3000000000
a: 1294967296, b: 1Total Area: -1294967294
```

解决办法，手工排序。

```java
public class Solution {
    public int computeArea(int A, int B, int C, int D, int E, int F, int G, int H) {
        int dup = 0;
        if(C < E || G < A || D < F || H < B){
            dup = 0;
        } else {
            int[] x = {A, C, E, G};
            int[] y = {B, D, F, H};
            Arrays.sort(x);
            Arrays.sort(y);
            dup = (x[2] - x[1]) * (y[2] - y[1]);
        }
        return (C - A) * (D - B) + (G - E)*(H - F) - dup;
    }
}
```
