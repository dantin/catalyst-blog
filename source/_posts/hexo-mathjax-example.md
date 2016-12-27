---
title: Mathjax的一些常用例子
date: 2016-12-27 10:58:01
categories: 效率
tags: [Hexo]
toc: true
mathjax: true
---

本文记录Mathjax的示例。

### 排版

{% math %}
\begin{aligned}
\left [ - \frac{\hbar^2}{2 m} \frac{\partial^2}{\partial x^2} + V \right ] \Psi
= i \hbar \frac{\partial}{\partial t} \Psi
\end{aligned}
{% endmath %}

### 数学方程

$g\frac{d^2u}{dx^2} + L\sin u = 0$
{% math %}
\begin{aligned}
J_\alpha(x) = \sum\limits_{m=0}^\infty \frac{(-1)^m}{m! \, \Gamma(m + \alpha + 1)}{\left({\frac{x}{2}}\right)}^{2 m + \alpha}
\end{aligned}
{% endmath %}

### 柯西不等式

{% math %}
\begin{aligned}
\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)
\end{aligned}
{% endmath %}

### 二项分布概率
$P(X=k)   = C^k_n p^k (1-p)^{n-k}$

### 麦克斯韦方程

{% math %}
\begin{aligned}
\nabla \times \vec{\mathbf{B}} -\, \frac1c\, \frac{\partial\vec{\mathbf{E}}}{\partial t} = \frac{4\pi}{c}\vec{\mathbf{j}} \\   \nabla \cdot \vec{\mathbf{E}} = 4 \pi \rho \\
\nabla \times \vec{\mathbf{E}}\, +\, \frac1c\, \frac{\partial\vec{\mathbf{B}}}{\partial t} = \vec{\mathbf{0}} \\
\nabla \cdot \vec{\mathbf{B}} = 0
\end{aligned}
{% endmath %}

### Latex使用

加减乘除：$a+b-c\times d+\frac{e}{f}\div g$

平方根：$\sqrt{n} $

求和：$\sum_{k=1}^n k$

求积：$\prod_{k=1}^n k$

微分：$\frac{d}{dx}\left(x^2\right) = 2x $

积分：$\int 2x \,dx = x ^ 2 + C \quad \int^5_1 2x \,dx = 24$

极限：$\lim_{x\to\infty}\frac{1}{x} $

数学函数：$\sin x \quad \csc x \quad \cos x \quad \sec x \quad \tan x \quad \cot x \quad \arcsin \quad \arccos \quad \arctan \quad \log n^2 \quad \ln e$

排列和组合：$ A_m^n \quad C_m^n \quad \dbinom{n}{r} $

下划线和上划线：$ \overline{a+bi} \quad \underline{431} \quad \vec{x} \quad \bar{x} $

特殊函数：$ \inf \quad \max \quad \min \quad \gcd \quad \exp $

点：$ \dot{x} \quad \dots \quad \cdot \quad \cdots $
