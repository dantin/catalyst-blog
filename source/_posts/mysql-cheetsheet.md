title: MySQL Cheetsheet
date: 2016-03-31 10:58:58
categories: 工程
tags: [MySQL, Cheetsheet]
toc: true
---

本文记录MySQL的常用命令。

### Schema相关

```sql
# 创建DB
CREATE DATABASE <db_name>;

# 删除DB
DROP DATABASE <db_name>;
```

### 用户相关

```sql
# 创建User
CREATE USER '<user_name>'@'%' IDENTIFIED BY '<password>';

# 删除用户
DROP USER '<user_name>'@'%';

# 修改权限
GRANT SELECT,INSERT,UPDATE,DELETE ON <db_name>.* to '<user_name>'@'%' WITH GRANT OPTION;

# 修改密码
SET PASSWORD FOR '<user_name>'@'localhost' = PASSWORD('<password>');

# 更新权限
FLUSH PRIVILEGES;
```

### 查看相关

```sql
# MySQL中的所有用户
SELECT User FROM mysql.user;

# 列出MySQL中的数据库
show databases;

# 返回当前 MySQL用户名和机主名
SELECT USER();
```
