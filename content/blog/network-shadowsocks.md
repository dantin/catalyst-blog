+++
date = "2016-09-23T11:37:08+08:00"
title = "Shadowsocks备忘录"
categories = ["Misc"]
tags = ["Network"]
description = "本文记录Shadowsocks的安装及优化加速"
slug = "network-shadowsocks"
+++

最近网络形式越来越严峻，在日益高筑的围墙之下，掌握一门穿墙之术越来越成为需要。相对于VPN而已，Shadowsocks更为轻量级，安装配置过程极其简单。而客户端也可以在windows、mac、iOS和android上轻松运行，被人们所深深喜爱。下面说说[Shadowosocks](https://github.com/shadowsocks/shadowsocks)的安装和优化。

### 服务端安装

官方推荐Ubuntu 14.04 LTS作为服务器以便使用TCP Fast Open。服务器端的安装非常简单。

Debian / Ubuntu:

```bash
apt-get install python-pip
pip install shadowsocks
```

CentOS:

```bash
yum install python-setuptools && easy_install pip
pip install shadowsocks
```

然后直接在后台运行：

```bash
ssserver -p 8000 -k password -m rc4-md5 -d start
```

当然也可以使用配置文件进行配置，方法创建/etc/shadowsocks.json文件，填入如下内容：

```json
{
    "server":"my_server_ip",
    "server_port":8000,
    "local_address": "127.0.0.1",
    "local_port":1080,
    "password":"mypassword",
    "timeout":300,
    "method":"rc4-md5"
}
```

然后使用配置文件在后台运行：

```bash
ssserver -c /etc/shadowsocks.json -d start
```

如果要停止运行，将命令中的start改成stop。

__TIPS__: 加密方式推荐使用`rc4-md5`，因为RC4比AES速度快好几倍，如果用在路由器上会带来显著性能提升。旧的RC4加密之所以不安全是因为Shadowsocks在每个连接上重复使用key，没有使用IV。现在已经重新正确实现，可以放心使用。更多可以看[issue](https://github.com/clowwindy/shadowsocks/issues/178)。

### 客户端安装

[客户端安装](https://sourceforge.net/projects/shadowsocksgui/)比较入门，这里就不说了。

### 加速优化

下面介绍一种简单的优化方法，能够得到立竿见影的效果。

首先，将 Linux 内核升级到 3.5 或以上。

__第一步，增加系统文件描述符的最大限数__

编辑文件limits.conf

```bash
vi /etc/security/limits.conf
```

增加以下两行

```bash
* soft nofile 51200
* hard nofile 51200
```

启动shadowsocks服务器之前，设置以下参数

```bash
ulimit -n 51200
```

__第二步，调整内核参数__

修改配置文件/etc/sysctl.conf

```bash
fs.file-max = 51200

net.core.rmem_max = 67108864
net.core.wmem_max = 67108864
net.core.netdev_max_backlog = 250000
net.core.somaxconn = 4096

net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_tw_recycle = 0
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_keepalive_time = 1200
net.ipv4.ip_local_port_range = 10000 65000
net.ipv4.tcp_max_syn_backlog = 8192
net.ipv4.tcp_max_tw_buckets = 5000
net.ipv4.tcp_fastopen = 3
net.ipv4.tcp_rmem = 4096 87380 67108864
net.ipv4.tcp_wmem = 4096 65536 67108864
net.ipv4.tcp_mtu_probing = 1
net.ipv4.tcp_congestion_control = hybla
```

修改后执行 sysctl -p 使配置生效

参考

[Jark](http://wuchong.me/blog/2015/02/02/shadowsocks-install-and-optimize/)