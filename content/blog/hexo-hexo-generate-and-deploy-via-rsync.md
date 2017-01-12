+++
date = "2017-01-05T17:47:40+08:00"
title = "Hexo Generate问题与远程部署"
categories = ["Misc"]
tags = ["Hexo"]
description = "本文记录Node内存不够导致Hexo无法发布的问题"
slug = "hexo-hexo-generate-and-deploy-via-rsync"
+++

### 内存不足问题

今天在VPS上部署网站时发现无法生成静态文件，日志如下：

```console
hexo g
INFO  [hexo-inject] installing hotfix for hexojs/hexo#1791
INFO  [hexo-math] Using engine 'mathjax'
INFO  Start processing
INFO  Files loaded in 3.75 s
Killed
```

开启`--debug`查看发布过程，并无任何特殊的地方，初步怀疑是内存不够。

搬瓦工默认的内存是512M，且不能增加swap空间。

```console
free -m
              total        used        free      shared  buff/cache   available
Mem:            512           8         479          10          24         443
Swap:           256           6         249
```

本地生成静态文件时，node有时可以飙到780M。

```console
Processes: 276 total, 4 running, 272 sleeping, 2073 threads           18:03:55
Load Avg: 2.50, 2.26, 2.33  CPU usage: 35.90% user, 20.24% sys, 43.85% idle
SharedLibs: 115M resident, 32M data, 11M linkedit.
MemRegions: 147205 total, 2340M resident, 74M private, 552M shared.
PhysMem: 8059M used (3551M wired), 131M unused.
VM: 855G vsize, 621M framework vsize, 66972060(192) swapins, 69689716(34810) sw
Networks: packets: 5503295/2985M in, 3468121/986M out.
Disks: 7419878/349G read, 3498623/325G written.

PID    COMMAND      %CPU      TIME     #TH   #WQ  #PORTS MEM    PURG   CMPRS
85619  node         83.4      00:17.69 11/1  1    51     779M+  0B     164M-
```

无它，只能找别的办法。

### 使用rsync远程部署

好在[Hexo的部署](https://hexo.io/zh-cn/docs/deployment.html)方式多样，选择rsync。

安装

```console
npm install hexo-deployer-rsync --save
```

在Hexo中的`_config.yml`中添加Deploy配置：

```console
deploy:
  type: rsync
  host: 你 VPS 的 IP 地址或者域名
  user: 用户名
  root: 你想将 Hexo 生成的静态文件存放在 VPS 中的目录 例如: /www/hexo/blog/
  port: 你 VPS 的 ssh 端口号
  delete: true
  verbose: true
  ignore_errors: false
  # args: optional，据说是后面，可以增加rsync的参数
```
