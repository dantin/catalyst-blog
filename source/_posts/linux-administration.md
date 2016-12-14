title: Linux管理
date: 2014-10-31 09:47:46
categories: 工程
tags: Linux
toc: true
---

本文记录了Linux中常见的管理命令。

### 系统命令

#### 查看发行版

```bash
lsb_release -a
LSB Version:    core-2.0-noarch:core-3.2-noarch:core-4.0-noarch:core-2.0-x86_64:core-3.2-x86_64:core-4.0-x86_64:desktop-4.0-amd64:desktop-4.0-noarch:graphics-2.0-amd64:graphics-2.0-noarch:graphics-3.2-amd64:graphics-3.2-noarch:graphics-4.0-amd64:graphics-4.0-noarch
Distributor ID: SUSE LINUX
Description:    SUSE Linux Enterprise Server 11 (x86_64)
Release:    11
Codename:   n/a
```

### 用户权限相关

#### 将用户加入sudoer组

如，将david加入sudo组。

``` bash
# usermod -a -G sudo david
```

### 网络相关

### 安装net-tools

CentOS默认没有ifconfig，需要安装net-tools

```
sudo yum install net-tools
```

#### 修改host文件

Host文件常用于域名解析，存放在/etc/hosts

``` bash
127.0.0.1       localhost
127.0.1.1       iDebian688
#
# Work use
#
54.183.197.33   rpt.content.com
```

#### 防火墙开端口

防火墙文件位于/etc/sysconfig/iptables

``` bash
//增加
-A INPUT -m state --state NEW -m tcp -p tcp --dport 8081 -j ACCEPT
```

重启防火墙

``` bash
service iptables restart
```

#### 查看网卡

```
ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: venet0: <BROADCAST,POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN
    link/void
    inet 127.0.0.1/32 scope host venet0
    inet 144.168.60.135/32 brd 144.168.60.135 scope global venet0:0

ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: venet0: <BROADCAST,POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT
    link/void
```

#### 查看网卡状态

```
cat /proc/net/dev
Inter-|   Receive                                                |  Transmit
 face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
    lo:       0       0    0    0    0     0          0         0        0       0    0    0    0     0       0          0
venet0: 221917054  187467    0    0    0     0          0         0 32630222  128074    0    0    0     0       0          0
```

### 应用相关

#### 安装包

``` bash
apt-get install packagename
yum install packagename
```

#### 删除包

```
apt-get remove packagename
yum remove packagename
yum erase packagename
```

#### 安装deb文件

```
dpkg -i wps-office_8.1.0.3724~b1p2_i386.deb
```

#### 查看命令所在的包

```
yum provides command
yum whatprovides command
```

#### 查看包包含的命令

```
rpm -ql packagename

yum install yum-utils
repoquery --list packagename
```

### 显示相关

#### 安装字体

从Windows机器的`%windir%\fonts`目录找到相应字体，复制到Linux系统中的/usr/share/fonts文件夹中，并更新。

``` bash
# cp mtextra.ttf symbol.ttf webdings.ttf wingding.ttf WINGDNG2.TTF WINGDNG3.TTF /usr/share/fonts
/* 生成字体的索引信息 */
# mkfontscale
# mkfontdir
/* 更新字体缓存 */
# fc-cache
```

### 基本概念

#### 运行级别介绍

在/etc/inittab里面看,下面的定义并不是标准配置，随着Debian版本的改变而改变。

一般2、3、4、5都是自定义的，具体看系统服务在2、3、4、5哪个级别运行。

比如gdm在5运行，那就是5是图形界面，如果gdm在2、3、4、5都运行，那么所有的2、3、4、5开机都会启动图形界面

* 0，停机
* 1，单用户模式
* 2，多用户，没有NFS
* 3，完全多用户模式
* 4，不知道
* 5，图形界面
* 6，重新启动

#### 自动运行机制

Linux发行版的/etc目录下，有init.d目录，和rc.local。它们都放着开机后自动运行的脚本。

/etc/rc(n).d目录（如：rc0.d, rc1.d, .... rc(n).d）实质上放着类似快捷方式的链接文件。指向init.d中的脚本。

如果想添加一个自动运行的脚本，先在/etc/init.d目下新建一个，脚本语言可以是python或sh。

具体的格式可以参见/etc/init.d目录中的一些例子。

关键是：

``` bash
update-rc.d  scriptname  start 99 2 3 4 5 stop 01 0 1 6
```

其中：

* scriptname ，就是自动运行的脚本的名字
* start 后面的一个参数 ，是启动的运行顺序  ，后面的2 3 4 5 （可多可少） 为在哪几个级别中运行(Debian 没有图形界面时， 默认是2）
* stop 同stop ，是关关机时运行的顺序，后面的（0 1 6） 也是运行级别。

例子：Debian wheezy 里边要添加一个自动启动的服务

先将启动脚本放在/etc/init.d，然后使用insserv来启用这个服务

例如服务名称为 myserver，则脚本为/etc/init.d/myserver

然后使用insserv myserver可以将myserver设为自动启动

``` bash
insserv myserver #添加服务
insserv -r myserver #删除服务
insserv -d myserver #使用默认的runlevels
```

脚本里边要定义启动文件的metadata，格式

``` bash
#!/bin/bash
#
### BEGIN INIT INFO
# Provides:          mysql
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Should-Start:      $network $time
# Should-Stop:       $network $time
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start and stop the mysql database server daemon
# Description:       Controls the main MySQL database server daemon "mysqld"
#                    and its wrapper script "mysqld_safe".
### END INIT INFO
#
```

#### 常用目录

* 应用程序目录：`/usr/share/applications`
* 配置目录：`/etc`

参考

* [Debian自动运行机制](http://www.cnblogs.com/wpjsolo/archive/2012/01/19/2327430.html)