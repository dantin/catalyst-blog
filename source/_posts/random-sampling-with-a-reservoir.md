---
title: 水塘抽样
date: 2016-12-07 21:49:01
categories: 学术
tags: Algorithm
toc: true
---

水塘抽样是一系列的随机算法，其目的在于从包含n个项目的集合S中选取k个样本，其中n为一很大或未知的数量，尤其适用于不能把所有n个项目都存放到主内存的情况。

### 算法

算法包含以下步骤（假设S以0开始标示）：

```
从S中抽取首k项放入「水塘」中
对于每一个S[j]项（j ≥ k）：
   随机产生一个范围从0到j的整數r
   若r < k，把水塘中的第r项替换成S[j]项
```

### 证明

假设k=1，第n项被抽中的概率是1/n，用P(n)表示。若项目共有N行，任意第n行被抽取的概率：

```
P(n) * multi(1-P(j))
= (1/n) * multi(1 - 1/j)
= (1/n) * (n / (n + 1)) * ... ((N - 1)/N)
= 1/N
```

各行被抽取的概率均相同。

当k>1时，循环内被抽中的概率是k/n，用P(n)表示。若项目共有N行，任意第n行被抽取的概率：

```
P(n) * multi(1-P(j)/k)
= (k/n) * multi(1 - k/(kj))
= (k/n) * (n / (n + 1)) * ... ((N - 1)/N)
= k/N
```

### 代码

```python
/*
  S has items to sample, R will contain the result
*/
ReservoirSample(S[1..n], R[1..k])
  // fill the reservoir array
  for i = 1 to k
      R[i] := S[i]
 
  // replace elements with gradually decreasing probability
  for i = k+1 to n
    j := random(1, i)   // important: inclusive range
    if j <= k
        R[j] := S[i]
```

证明见[wikipedia](https://zh.wikipedia.org/wiki/水塘抽樣)