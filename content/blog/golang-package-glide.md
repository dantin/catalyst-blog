+++
title = "Golang的包管理器Glide"
categories = ["Engineering"]
tags = ["Golang"]
description = "本文记录Glide的包管理工具"
slug = "golang-package-glide"
date = "2017-08-07T10:40:32+08:00"
+++

Golang的包管理工具有很多，本篇幅主要介绍Glide。


### 安装

```console
brew install glide
go get github.com/Masterminds/glide
```

### 命令介绍

```console
# 初始化项目并创建glide.yaml文件
glide create|init.
# 安装包
glide install
# 更新包
glide update|up
# 获取单个包
glide get
```

其中`get`比较Trick：

* `--all-dependencies`：会下载所有关联的依赖包
* `-s`：删除所有版本控制，如`.git`
* `-v`：删除嵌套的vendor

获得制定版本的包：

```console
glide get github.com/go-sql-driver/mysql#v1.2
```

### 团队开发

在团队开始时，需要将`glide.yaml`和`glide.lock`进行版本控制，`vendor`忽略掉。

模拟下团队开发的流程

A同学：初始化项目，并提交了源码，其中包含`glide.yaml`和`glide.lock`

B同学：拉去项目，执行`glide install`，会自动下载对应的包

参考

[官方文档](https://glide.readthedocs.io/en/latest/)
