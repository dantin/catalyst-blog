title: Hello World
date: 2014-10-17 15:08:58
categories: 学习
tags: Hexo
toc: true
---
[Hexo](http://hexo.io/)是一个简单、轻量的静态博客框架，基于Nodejs。

Hexo的[文档](http://hexo.io/docs/)丰富，社区完善。由于作者是台湾人，所以一些[中文问题](http://hexo.io/docs/troubleshooting.html)的定位和解决方便许多。:D

## 安装

首先确保Nodejs和Git都安装好。

``` bash
npm install -g hexo
```

### 创建工程目录

``` bash
hexo init <folder>
cd <folder>
hexo init
```

## 使用入门

### 新建文章

``` bash
hexo new "My New Post"
```

More info: [Writing](http://hexo.io/docs/writing.html)

### 启动服务器

``` bash
hexo server
```

More info: [Server](http://hexo.io/docs/server.html)

### 生成静态文件

``` bash
hexo generate
```

More info: [Generating](http://hexo.io/docs/generating.html)

### 部署

``` bash
hexo deploy
```

More info: [Deployment](http://hexo.io/docs/deployment.html)

## 主题安装

安装主题和渲染器：

``` bash
git clone https://github.com/tufu9441/maupassant-hexo.git themes/maupassant
npm install hexo-renderer-sass --save
npm install hexo-renderer-jade --save
```

编辑Hexo目录下的 _config.yml，将theme的值改为maupassant。

主题的配置文件在```themes/maupassant/_config.yml```

## 参考

1. [GitHub](https://github.com/hexojs/hexo/issues)
2. [maupassant主题](https://www.haomwei.com/technology/maupassant-hexo.html)