+++
date = "2016-03-31T10:23:03+08:00"
title = "安装MySQL"
categories = ["Engineering"]
tags = ["MySQL"]
description = "本文记录Mac上MySQL的安装过程"
slug = "mysql-installation"
+++

### 安装

#### MacOS

直接使用`brew`安装。

```bash
brew install mysql
==> Downloading https://homebrew.bintray.com/bottles/mysql-5.7.9.el_capitan.bottle.tar.gz

curl: (35) Server aborted the SSL handshake
Error: Failed to download resource "mysql"
Download failed: https://homebrew.bintray.com/bottles/mysql-5.7.9.el_capitan.bottle.tar.gz
Warning: Bottle installation failed: building from source.
==> Downloading https://cdn.mysql.com/Downloads/MySQL-5.7/mysql-5.7.9.tar.gz
Already downloaded: /Library/Caches/Homebrew/mysql-5.7.9.tar.gz
==> cmake . -DCMAKE_INSTALL_PREFIX=/usr/local/Cellar/mysql/5.7.9 -DCMAKE_FIND_FRAMEWORK=LAST -DCMAKE_VERBOSE_MAKEFILE=ON -DMYSQL_DATADIR=/usr/local/var/mysql -DINSTALL_INCLUDEDIR=include/mysql -DINSTALL_M
==> make
==> make install
==> /usr/local/Cellar/mysql/5.7.9/bin/mysqld --initialize --user=w3 --basedir=/usr/local/Cellar/mysql/5.7.9 --datadir=/usr/local/var/mysql --tmpdir=/tmp
==> Caveats
A "/etc/my.cnf" from another install may interfere with a Homebrew-built
server starting up correctly.

To connect:
    mysql -uroot

To have launchd start mysql at login:
  ln -sfv /usr/local/opt/mysql/*.plist ~/Library/LaunchAgents
Then to load mysql now:
  launchctl load ~/Library/LaunchAgents/homebrew.mxcl.mysql.plist
Or, if you don't want/need launchctl, you can just run:
  mysql.server start
==> Summary
🍺  /usr/local/Cellar/mysql/5.7.9: 12629 files, 464M, built in 6.4 minutes
```

#### Linux

通过`tar.gz`文件安装。

```bash
# 下载64-bit版本
wget -c https://dev.mysql.com/get/Downloads/MySQL-5.6/mysql-5.6.35-linux-glibc2.5-x86_64.tar.gz
# 创建用户
groupadd MySQL
useradd -r -g MySQL MySQL
# 解压
mkdir -p /opt/mysql
tar zxvf mysql-5.6.35-linux-glibc2.5-x86_64.tar.gz -C /opt/mysql/
# 软链接
cd /usr/local/
ln -s /opt/mysql/mysql-5.6.35-linux-glibc2.5-x86_64/ MySQL
# 安装
cd MySQL/
chown -R MySQL .
chgrp -R MySQL .
scripts/mysql_install_db --user=MySQL
chown -R root .
chgrp -R MySQL data
# optional
# 此时my.cnf已经复制完毕
cat /etc/my.cnf
# 启动
bin/mysqld_safe --user=MySQL
# 开机启动
cp support-files/mysql.server /etc/init.d/mysql.server
```

### 配置

有些版本升级完成后，MySQL的配置发生改变，需要用默认值覆盖老的配置文件`/etc/my.cnf`。

```bash
sudo cp /usr/local/opt/mysql/support-files/my-default.cnf /etc/my.cnf
```

但是使用`mysql.server start`启动后，使用`mysql -uroot`提示访问被阻止。

解决方案:

重新生成默认配置。（P.S. 升级后出现问题，也能按照这个办法解决）

```bash
mysql.server stop
rm -r /usr/local/var/mysql
mysqld --initialize --user=`whoami` --basedir="$(brew --prefix mysql)" --datadir=/usr/local/var/mysql --tmpdir=/tmp
```

输出的最后一行:

```bash
2016-03-31T02:07:05.228433Z 0 [Warning] CA certificate ca.pem is self signed.
2016-03-31T02:07:05.340712Z 1 [Note] A temporary password is generated for root@localhost: jbp6V3JD8+g:
```

冒号后面的就是密码，这里是`jbp6V3JD8+g:`。

我们自己的本机不需要这么复杂的密码, 改成简单的密码。

```bash
mysql.server start
mysql -uroot -h 127.0.0.1 -p
```

登录后执行如下SQL语句：

```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY '123456';
```

输入旧的密码后就可以把密码改成123456了

ps: 安装的密码看`~/.mysql_secret`

### 问题

#### 权限问题

启动如果报错，通常是MySQL启动的时候要默认创建一些日志文件，或者运行相关的文件，但是没有创建，或者指定的目录不存在，常见的有：

1. `/var/log/mariadb/mariadb.log`不存在或文件没有权限
2. `/var/run/mariadb/mariadb.pid`不存在或文件没有权限

需要分别要创建两个目录

```bash
mkdir /var/log/mariadb
mkdir /var/run/mariadb
chown MySQL -R /var/run/mariadb
chown MySQL -R /var/log/mariadb
```

当然以上配置均可以修改`my.cnf`配置文件来修改其位置

#### 客户端启动不了

症状一般是：

```bash
ERROR 2002 (HY000): Can’t connect to local MySQL server through socket ‘/tmp/mysql.sock’ (2)
```

此错误是因为socket位置导致

查看`/etc/my.cnf`，如下：

```console
[mysql]
socket=/var/lib/mysql/mysql.sock
```

加个软链, 当然修改`/etc/my.cnf`的sock位置也可以

```bash
ln -s /var/lib/mysql/mysql.sock /tmp/mysql.sock
```

#### Root密码问题

安装好MySQL后提示要输入密码。

```bash
mysql -u root -p
Enter password:
ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: NO)
```

从MySQL5.6.8开始，MySQL RPM安装包用了更安全的安装方式，再不是以前的密码为空了，`MySQL`会给root账号随机分配一个密码，安装`MySQL`后，root的这个随机密码会写在文件：`~/.mysql_secret`中，但这个密码不能做任何事情，只能登录。然后必须更改密码才能正常使用。

使用就安全模式登入。

```bash
/etc/init.d/mysql.server stop
mysqld_safe --user=MySQL --skip-grant-tables

# 客户端
mysql -u root -p
# 回撤进入
mysql> SET Password=PASSWORD('newpassword')
mysql> FLUSH PRIVILEGES;
```
