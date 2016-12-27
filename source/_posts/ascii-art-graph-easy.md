---
title: 基于纯文本的流程图
date: 2016-12-27 13:54:49
category: 效率
tags: ASCII
toc: true
---

纯文本可以写代码，可以写文档（Markdown），那么对于更直观的信息表达方式，图片，能不能也用纯文本描述呢？

本文主要关注基于纯文本的流程图。

### 简介

Graph::Easy就是本文的主角，它是perl的一个软件包，可以使用perl代码直接描述图像；当然，我们肯定不会为了画个图专门去学习perl;

这个软件包的强大之处在于，它定义了一套非常简单易用的专门用来描述图像的DSL（领域专用语言）,我们可以像写代码一样表达我们需要描述的图像；不用关心图像里面如何布局；这种语言经过处理可以得到ASCII图像，直接放在代码注释中；如果需要还可以转换成png或者矢量图等格式。

先举个简单的例子，感受一下:

```
[ Bonn ] --> [ Koblenz ] --> [ Frankfurt ] --> [ Dresden ]

[ Koblenz ] --> [ Trier ] { origin: Koblenz; offset: 2, 2; }
  --> [ Frankfurt ]
```

这种DSL经过渲染之后得到的ASCII图是这样的：

```
+------+     +---------+                   +-----------+     +---------+
| Bonn | --> | Koblenz | ----------------> | Frankfurt | --> | Dresden |
+------+     +---------+                   +-----------+     +---------+
               |                             ^
               |                             |
               |                             |
               |             +-------+       |
               +-----------> | Trier | ------+
                             +-------+
```

### 安装

下面介绍安装过程：

1. 首先需要安装graphviz软件包
    可以在[graphviz官网](http://www.graphviz.org/)下载；
    Mac用户可以`brew install graphviz`；
    其他linux发行版参考官网。
2. 安装perl
    mac和linux用户可以略过；一般系统自带；
    windows去perl官网查询如何安装; 据说windows下有傻瓜包activeperl；
3. 安装cpan
    这个是perl的软件包管理，类似npm, pip, apt-get;
    Mac下直接在命令行输入`cpan`命令，一路next即可。
    其他系统参考[cpan官网](http://www.cpan.org/modules/INSTALL.html)
4. 安装Graph::Easy
    命令行输入`cpan`进入cpan shell；
    输入`install Graph::Easy`即可。

### 使用

使用分为两步

1. 使用Graph::Easy DSL的语法描述图像，存为文本文件，比如`simple.txt`
2. 使用 graph-easy 命令处理这个文件：`graph-easy simple.txt`

最简单的使用方式就是这样；当然，Graph::Easy不仅仅支持自己的DSL语法，它还支持诸如dot这种较为通用的图像描述语言；可以直接读取dot 格式的输入，产生其他的诸如ascii，png，svg格式的图像。

### 语法

#### 注释

注释用`#`表达；

__注意__

1. `#`之后，一定需要加空格；
2. 由于历史原因；Graph::Easy的颜色也使用了`#`，不加空格会解析失败。

```
##############################################################
# 合法的注释

##############################################################
#有问题的注释

node { label: \#5; }      # 注意转义！
edge { color: #aabbcc; }  # 可以使用颜色值
```

#### 空格

空格通常没有什么影响，多个空字符会合并成一个，换行的空字符会忽略；下面的表述是等价的。

```
[A]->[B][C]->[D]
```

```
[ A ] -> [ B ]
[ C ] -> [ D ]
```

#### 节点(Node)

用中括号括起来的就是节点，我们简单可以理解为一些形状；比如流程图里面的矩形，圆等；

```
[ Single node ]
[ Node A ] --> [ Node B ]
```

可以用逗号分割多个节点：

```
[ A ], [ B ], [ C ] --> [ D ]
```

上面的代码图像如下：

```
+---+     +---+     +---+
| A | --> | D | <-- | C |
+---+     +---+     +---+
            ^
            |
            |
          +---+
          | B |
          +---+
```

#### 边(Edges)

将节点连接起来的就是边；Graph::Easy 的DSL支持这几种风格的边：

```
->              实线
=>              双实线
.>              点线
~>              波浪线
- >             虚线
.->             点虚线
..->            dot-dot-dash
= >             double-dash
```

可以给边加标签，如下：

```
[ client ] - request -> [ server ]
```

结果如下：

```
+--------+  request   +--------+
| client | ---------> | server |
+--------+            +--------+
```

#### 属性(Attributes)

可以给节点和边添加属性；比如标签，方向等；使用大括号`{}`表示，里面的内容类似css，`attribute: value`。

```
[ "Monitor Size" ] --> { label: 21"; } [ Big ] { label: "Huge"; }
```

上面的DSL输入如下：

```
+----------------+  21"   +------+
| "Monitor Size" | -----> | Huge |
+----------------+        +------+
```

Graph::Easy提供了非常多的属性; 另外，Graph::Easy的[文档](http://bloodgate.com/perl/graph/manual/index.html)非常详细，建议通读一遍；了解其中的原理和细节，对于绘图和布局有巨大帮助。

### 实例

语法是不是非常简单？有了这些知识，我们就可以建立自己的流程图了；

新建文件，输入以下代码：

```txt
[ View ] {rows:3} - Parse calls to -> [ Presenter ] {flow: south; rows: 3} - Manipulates -> [ Model ]
[ Presenter ] - Updates -> [ View ]
```

保存然后退出；命令行执行`graph-easy mvp.txt`, 输入效果如下：

```
+------+  Parse calls to   +--------------+
|      | ----------------> |              |
| View |                   |  Presenter   |
|      |  Updates          |              |
|      | <---------------- |              |
+------+                   +--------------+
                             |
                             | Manipulates
                             v
                           +--------------+
                           |    Model     |
                           +--------------+
```

两行代码就搞定了！自动对齐，调整位置，箭头，标签等等；我们完全不用管具体图形应该如何绘制，注意力集中在描述图像本身。
