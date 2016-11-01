---
title: Proxychains的安装和使用
date: 2016-10-27 09:51:45
categories: 工程
tags: Network
toc: true
---

安装了shadowsocks之后，只能网页出去逛逛，如果需要在command Line中也能有同样的效果，需要配合proxychains。

### 安装

安装proxychains比较简单

```bash
git clone https://github.com/rofl0r/proxychains-ng.git
cd proxychains-ng
./configure
(sudo) make && make install
cp ./src/proxychains.conf /etc/proxychians.conf
cd .. && rm -rf proxychains-ng
```

或者直接用homebrew安装。

```bash
brew install proxychains-ng
```

### 修改配置

修改配置`/usr/local/etc/proxychains.conf`如下：

```bash
strict_chain
proxy_dns
remote_dns_subnet 224

# Some timeouts in milliseconds
tcp_read_time_out 15000
tcp_connect_time_out 8000

[ProxyList]
# add proxy here ...
# meanwile
# defaults set to "tor"
socks5  127.0.0.1 1080
```

### 使用

在命令行前加proxychains4。

```bash
proxychains4 curl https://www.twitter.com/
proxychains4 git push origin master
```
