+++
date = "2017-03-21T15:53:48+08:00"
title = "Gradle常用命令备忘录"
categories = ["Engineering"]
tags = ["Gradle", "Memo"]
description = "本文记录Gradle的常用命令"
slug = "gradle-memo"
+++

### 安装

在[Gradle.org](https://gradle.org/)下载二进制发行版。

解压并安装

```bash
mkdir /opt/gradle
unzip -d /opt/gradle gradle-3.4.1-bin.zip
ls /opt/gradle/gradle-3.4.1
LICENSE  NOTICE  bin  getting-started.html  init.d  lib  media
```

配置系统环境

```bash
export PATH=$PATH:/opt/gradle/gradle-3.4.1/bin
```

验证

```bash
$ gradle -v

------------------------------------------------------------
Gradle 3.4.1
------------------------------------------------------------
```
