---
title: 安装MySQL
date: 2016-03-31 10:23:03
categories: 工程
tags: MySQL
toc: true
---

本文记录Mac中安装MySQL的步骤。

### 安装

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
