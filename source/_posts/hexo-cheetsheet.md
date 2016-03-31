title: Hexo Cheetsheet
date: 2016-01-20 09:56:45
categories: 工程
tags: [Hexo, Cheetsheet]
toc: true
---

本文记录Hexo的常用方法。

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
