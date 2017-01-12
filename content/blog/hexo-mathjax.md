+++
date = "2016-12-13T15:02:33+08:00"
title = "使用hexo-math插件让Hexo支持MathJax"
categories = ["Misc"]
tags = ["Hexo","Mathjax"]
description = "本文记录Hexo整合Mathjax的方法"
slug = "hexo-mathjax"
+++

MathJax是使用LaTeX方式输入数学公式的好工具。Hexo虽然可以直接使用mathjax，但是存在一些不方便之处。使用[hexo-math](https://github.com/akfish/hexo-math)这个插件可以大大方便使用。

### 安装

在hexo安装目录下执行

```console
# 可能的依赖
npm install hexo-inject --save
npm install hexo-math --save
```

### 配置

编辑站点根目录下的_config.yml，添加

```console
math:
  engine: 'mathjax' # or 'katex'
  mathjax:
    src: custom_mathjax_source
    config:
      # MathJax config
```

进入theme的目录，编辑主题的_config.yml，找到mathjax字段。

```console
mathjax:
   enable: true
```

最后hexo g，就可以部署或者运行server查看效果了。

_注意_：在对应的md页面中需要指明

```console
...
mathjax: true
```

参考：

* [zjubank.com](http://zjubank.com/2016/08/16/hexo-use-mathjax/)
* [MathJax不同用法的对比](http://lukang.me/2014/mathjax-for-hexo.html)
* [Latex的手写识别](http://detexify.kirelabs.org/classify.html)
* [MathJax支持的Tex命令](http://www.onemathematicalcat.org/MathJaxDocumentation/TeXSyntax.htm)
* [MathJax基础教程](http://meta.math.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference)
* [MathJax文档](http://docs.mathjax.org/en/latest/index.html)
