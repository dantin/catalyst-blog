+++
date = "2016-03-31T10:58:58+08:00"
title = "MySQL常用命令备忘录"
categories = ["Engineering"]
tags = ["MySQL", "Cheetsheet"]
description = "本文记录MySQL的常用命令"
slug = "mysql-memo"
+++

### 连接

```bash
# TCP/IP套接字连接
mysql -h 127.0.0.1 -u root -p

# UNIX套接字连接
mysql -uroot -S /tmp/mysql.sock  -p
```

### Schema相关

```sql
# 创建DB
CREATE DATABASE <db_name>;

# 删除DB
DROP DATABASE <db_name>;

# 重命名表名
RENAME TABLE tbl_name TO new_tbl_name;
```

### 用户相关

```sql
# 创建User
CREATE USER '<user_name>'@'%' IDENTIFIED BY '<password>';

# 删除用户
DROP USER '<user_name>'@'%';

# 修改权限
# GRANT <privileges> ON <what> TO <user> [IDENTIFIED BY "<password>"] [WITH GRANT OPTION];
GRANT SELECT,INSERT,UPDATE,DELETE ON <db_name>.* to '<user_name>'@'%' WITH GRANT OPTION;

# 修改密码
SET PASSWORD FOR '<user_name>'@'localhost' = PASSWORD('<password>');

# 更新权限
FLUSH PRIVILEGES;

# 查看用户权限
SHOW GRANTS FOR 'root'@'%';
```

### 查看相关

```sql
# MySQL中的所有用户
SELECT User FROM mysql.user;

# 显示当前用户可见的所有库
SHOW databases;
# 从数据字典里面看当前有进程链接的库
SELECT DISTINCT db FROM information_schema.processlist;

# 返回当前 MySQL用户名和机主名
SELECT USER();

# 返回当前使用的数据库
SELECT DATABASE();
```

### 数据导入

```sql
# 倒入file.csv到某张表
load data local infile '/directory/file.csv'
into table fdd_esf_push.temp_device_info
fields terminated by ','  enclosed by '"'
lines terminated by '\r\n';

# 导出
$ mysqldump -h host_name -u username -p database > file.sql
# 导入
create database aaa;
use aaa;
source ./file.sql
```
