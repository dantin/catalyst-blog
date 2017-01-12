+++
date = "2016-01-27T13:19:35+08:00"
title = "Scala安装记录"
categories = ["Engineering"]
tags = ["Scala"]
description = "本文记录Scala的安装过程"
slug = "scala-installation"
+++

本文记录Linux中安装Scala的步骤。

### 安装准备

下载[Scala](http://www.scala-lang.org/download/)

### 安装Scala

#### CentOS

执行以下操作：

``` bash
cd /opt
tar -zxvf scala-2.11.7.tgz
```

### 配置环境变量

修改系统环境变量文件`/etc/profile`，追加以下内容：

``` bash
#SCALA
export SCALA_HOME=/opt/scala-2.11.7
export PATH=$PATH:$SCALA_HOME/bin
```

强制修改生效

``` bash
source /etc/profile   //使修改立即生效 
echo $PATH            //查看PATH值
```

### 验证

执行以下操作，查看信息是否正常：

``` bash
scala -version
Scala code runner version 2.11.7 -- Copyright 2002-2013, LAMP/EPFL
```

恭喜，安装成功！
