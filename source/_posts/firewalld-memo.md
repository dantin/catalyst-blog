---
title: Firewalld备忘录
date: 2016-12-11 23:01:34
categories: 效率
tags: [Linux, Network]
toc: true
---

firewalld是centos7的一大特性，最大的好处有两个：支持动态更新，不用重启服务；第二个就是加入了防火墙的“zone”概念。

### 常用命令

永久开关一个端口

```
firewall-cmd --permanent --add-port=8080/tcp
firewall-cmd --permanent --remove-port=8080/tcp
```

永久开关某项服务

```
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --remove-service=http
```

进行端口转发

```
firewall-cmd --permanent --add-forward-port=port=80:proto=tcp:toport=8080:toaddr=192.0.2.55
```

允许转发到其他地址

```
firewall-cmd --permanent --add-masquerade
```

重新加载防火墙

```
firewall-cmd --reload
```

### 运维相关

```
# 启动
systemctl start firewalld
# 查看状态
systemctl status firewalld
firewall-cmd –state
# 停止
systemctl disable firewalld
# 禁用
systemctl stop firewalld
```

### 配置相关

```
# 查看版本
firewall-cmd –version
# 查看帮助
firewall-cmd –help

# 查看设置
# 显示状态
firewall-cmd –state
# 查看区域信息
firewall-cmd –get-active-zones
# 查看指定接口所属区域
firewall-cmd –get-zone-of-interface=eth0

# 拒绝所有包
firewall-cmd –panic-on
# 取消拒绝状态
firewall-cmd –panic-off
# 查看是否拒绝
firewall-cmd –query-panic
```
