title: 可以发Tweet的数字艺术照片
date: 2015-12-30 12:32:19
categories: 网摘
tags: 程序员
toc: true
---

### 简介

[PPM](https://en.wikipedia.org/wiki/Netpbm_format)，是一种图像格式，全称为：可移植像素图格式(PPM)。另外两种类似的格式是可移植灰度图格式(PGM)和可移植位图格式(PBM)，可以跨平台。它们三个也被统称为PNM格式。

#### 文件格式描述[编辑]

这三种格式在颜色的表示上有差异。PBM是单色，PGM是灰度图，PPM使用RGB颜色。

每个文件的开头两个字节（ASCII码）作为文件描述子，指出具体格式和编码形式。具体见下表。

文件描述子 | 类型 | 编码
---|---|---
P1 | 位图 | ASCII
P2 | 灰度图 | ASCII
P3 | 像素图 | ASCII
P4 | 位图 | 二进制
P5 | 灰度图 | 二进制
P6 | 像素图 | 二进制

基于ASCII的格式使人可读，并且能够很容易的移植到其他格式。但是二进制格式更有效，不仅因为他节约空间，而且因为他更容易被解析（因为很少有空格）

当使用二进制格式的时候，PBM每像素使用一个比特空间，PGM每个像素使用8个比特空间，PPM每像素使用24比特空间（8比特红色、8比特绿色、8比特蓝色）。

#### 例子
下面是一个PBM简单的例子

``` bash
P1
# This is an example bitmap of the letter "J"
# column row
6 10
0 0 0 0 1 0
0 0 0 0 1 0
0 0 0 0 1 0
0 0 0 0 1 0
0 0 0 0 1 0
0 0 0 0 1 0
1 0 0 0 1 0
0 1 1 1 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```

P1表示文件格式。#符号表示一个注释。接下来两个数是宽度和高度。接下来的矩阵是每个像素的值。(在这里单色格式，只有0和1）

### 艺术照片

有了上述概念后，看一下Kyle McCormick 在 StackExchange 上发起的一个叫做[Tweetable Mathematical Art](http://codegolf.stackexchange.com/questions/35569/tweetable-mathematical-art)的比赛。

参赛者需要用三条推这么长的代码来生成一张图片。具体地说，参赛者需要用 C++ 语言编写 RD 、 GR 、 BL三个函数，每个函数都不能超过 140 个字符。每个函数都会接到 i 和 j 两个整型参数（0 ≤ i, j ≤ 1023），然后需要返回一个 0 到 255之间的整数，表示位于 (i, j) 的像素点的颜色值。举个例子，如果 RD(0, 0) 和 GR(0, 0) 返回的都是 0 ，但 BL(0, 0)返回的是 255 ，那么图像的最左上角那个像素就是蓝色。参赛者编写的代码会被插进下面这段程序当中（我做了一些细微的改动），最终会生成一个大小为1024×1024 的图片。

#### 代码框架

``` cpp
// NOTE: compile with g++ filename.cpp -std=c++11
 
#include <iostream>
#include <cmath>
#include <cstdlib>
#define DIM 1024
#define DM1 (DIM-1)
#define _sq(x) ((x)*(x)) // square
#define _cb(x) abs((x)*(x)*(x)) // absolute value of cube
#define _cr(x) (unsigned char)(pow((x),1.0/3.0)) // cube root
 
unsigned char GR(int,int);
unsigned char BL(int,int);
 
unsigned char RD(int i,int j){
// YOUR CODE HERE
}
unsigned char GR(int i,int j){
// YOUR CODE HERE
}
unsigned char BL(int i,int j){
// YOUR CODE HERE
}
 
void pixel_write(int,int);
FILE *fp;
int main(){
fp = fopen("MathPic.ppm","wb");
fprintf(fp, "P6\n%d %d\n255\n", DIM, DIM);
for(int j=0;j<DIM;j++)
for(int i=0;i<DIM;i++)
pixel_write(i,j);
fclose(fp);
return 0;
}
void pixel_write(int i, int j){
static unsigned char color[3];
color[0] = RD(i,j)&255;
color[1] = GR(i,j)&255;
color[2] = BL(i,j)&255;
fwrite(color, 1, 3, fp);
}
```

#### 示例代码

```
unsigned char RD(int i,int j){
double a=0,b=0,c,d,n=0;
while((c=a*a)+(d=b*b)<4&&n++<880)
{b=2*a*b+j*8e-9-.645411;a=c-d+i*8e-9+.356888;}
return 255*pow((n-80)/800,3.);
}
 
unsigned char GR(int i,int j){
double a=0,b=0,c,d,n=0;
while((c=a*a)+(d=b*b)<4&&n++<880)
{b=2*a*b+j*8e-9-.645411;a=c-d+i*8e-9+.356888;}
return 255*pow((n-80)/800,.7);
}
 
unsigned char BL(int i,int j){
double a=0,b=0,c,d,n=0;
while((c=a*a)+(d=b*b)<4&&n++<880)
{b=2*a*b+j*8e-9-.645411;a=c-d+i*8e-9+.356888;}
return 255*pow((n-80)/800,.5);
}
```

编译

``` bash
g++ filename.cpp -std=c++11
```

#### 生成的图片

![数字艺术照片](/images/tweetable-mathematical-art.jpg "Tweetable-mathematical-art")



