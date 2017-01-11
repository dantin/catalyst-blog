+++
date = "2016-01-20T09:56:45+08:00"
title = "Hexo备忘录"
categories = ["Misc"]
tags = ["Hexo", "Memo"]
description = "本文记录Hexo的常用方法"
slug = "hexo-memo"
+++

### Hexo

``` Bash
# 安装
npm install hexo -g
# 升级
npm update hexo -g
# 初始化，生成文件夹为blog
hexo init blog
cd blog
# 安装依赖库
npm install
# 运行测试
hexo server
```

### 写作

``` Bash
# 新建草稿
hexo new draft "new draft"
# 变成正式文章
hexo publish [layout] <title>
```
