---
title: MySQL主从复制介绍及搭建
date: 2016-04-08 18:28:23
categories: 工程
tags: MySQL
toc: true
---

本文介绍MySQL主从复制及搭建的过程。

### 介绍

MySQL主从复制就是从一台MySQL数据库服务器（主服务器Master）复制日志到另一个服务器（从服务器Slave），然后解析日志并应用到自身的过程。类似Oracle中的Data Guard。

MySQL复制的好处：

* 解决宕机带来的数据不一致，MySQL复制可以实时备份数据；
* 减轻数据库服务器的压力，多台服务器的性能一般比单台要好。

_备注：MySQL复制不适合大数据量，大数据量推荐使用集群。_

MySQL复制过程分成三步：

1. Master将改变记录到二进制日志（Binary Log）。这些记录动作叫做二进制日志事件，Binary Log Events；
2. Slave将Master的Binary Log Events拷贝到它的中继日志（Relay Log）；
3. Slave重做中继日志中的事件，将Binary Log Events应用到自己的数据库中。 MySQL复制是异步的且串行化的；

![MySQL主从复制原理图](/images/mysql-master-slave-replication-1.png "MySQL Master Slave Replication")

### 搭建

#### 环境准备

实验环境

```bash
Master: 192.168.1.5
Slave:  192.168.1.6
OS:     Redhat Linux 6.1
MySQL:  5.5.37
```

#### Master配置

__1. 分配复制权限__

主库和从库均需要执行

```bash
mysql> grant replication client,replication slave on *.* to root@'192.168.1.%' identified by 'root';
Query OK, 0 rows affected (0.00 sec)
```

__2. 清空日志文件__
    
主从库都是默认开启二进制日志文件

```bash
mysql> show binary logs;
+------------------+-----------+
| Log_name         | File_size |
+------------------+-----------+
| mysql-bin.000001 |     26636 |
| mysql-bin.000002 |   1069399 |
| mysql-bin.000003 |     26636 |
| mysql-bin.000004 |   1069399 |
| mysql-bin.000005 |       536 |
+------------------+-----------+
5 rows in set (0.00 sec)

mysql> reset master;
Query OK, 0 rows affected (0.01 sec)

mysql> show binary logs;
+------------------+-----------+
| Log_name         | File_size |
+------------------+-----------+
| mysql-bin.000001 |       107 |
+------------------+-----------+
1 row in set (0.00 sec)
```

_注意_：如果不想清空日志文件的话，需要记录当前Master的log_file和log_pos，并在下面启用复制操作时指定这两个参数或者在Slave的配置文件指定。

#### Slave设置

__1. 修改从服务器server-id__

 ```bash
 # vim /etc/my.cnf
 server-id = 2
 ```

修改完以后需要重启数据库

__2. 清空日志文件，同Master__

__3. 启用复制__

 让Slave连接Master并开始重做Master二进制日志中的事件

 ```bash
 mysql> change master to 
 master_host='192.168.1.5',master_user='root',master_password='root',master_port=3306,master_log_file='mysql-bin.000001',master_log_pos=0;
 ```
 
 master_log_pos的值为0，因为它是日志的开始位置；master_log_file是初始日志文件。如果Master日志没有被清空，这里就是当前Master的日志信息。

 需要注意的是，默认情况下，会同步该用户下所有的DB，如果想限定哪些DB，有三种办法：

 * 在master上的/etc/my.inf中通过参数binlog-do-db、binlog-ignore-db设置需要同步的数据库。
 * 在执行grant分配权限操作的时候，限定数据库
 * 在slave上限定数据库使用`replicate-do-db=dbname`

__4. 开启Slave__

```bash
mysql> start slave;
Query OK, 0 rows affected (0.00 sec)
```

__5.确认Slave是否和Mater成功通信__

如果 Slave_IO_Running和Slave_SQL_Running都是yes，则证明配置成功

```bash
mysql> show slave status\G;
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 192.168.1.5
                  Master_User: root
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mysql-bin.000001
          Read_Master_Log_Pos: 107
               Relay_Log_File: rac-node2-relay-bin.000002
                Relay_Log_Pos: 253
        Relay_Master_Log_File: mysql-bin.000001
            **Slave_IO_Running: Yes**
            **Slave_SQL_Running: Yes**
              Replicate_Do_DB: 
          Replicate_Ignore_DB: 
           Replicate_Do_Table: 
       Replicate_Ignore_Table: 
      Replicate_Wild_Do_Table: 
  Replicate_Wild_Ignore_Table: 
                   Last_Errno: 0
                   Last_Error: 
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 107
              Relay_Log_Space: 413
              Until_Condition: None
               Until_Log_File: 
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File: 
           Master_SSL_CA_Path: 
              Master_SSL_Cert: 
            Master_SSL_Cipher: 
               Master_SSL_Key: 
        Seconds_Behind_Master: 0
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error: 
               Last_SQL_Errno: 0
               Last_SQL_Error: 
  Replicate_Ignore_Server_Ids: 
             Master_Server_Id: 1
1 row in set (0.00 sec)
```

### 测试

Master创建数据库

```bash
mysql> create database d;
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| d                  |
| mysql              |
| performance_schema |
| test               |
+--------------------+
```

Slave查看数据库已同步

```bash
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| d                  |
| mysql              |
| performance_schema |
| test               |
+--------------------+
```

Master创建表插入数据

```bash
mysql> use d
mysql> create table t(id int);
mysql> insert into t values(1);
mysql> commit;
```

Slave查看

```bash
mysql> use d;
mysql> show tables;
mysql> select * from t;
+------+
| id   |
+------+
|    1 |
+------+
```

通过以上验证，可以看到主服务器上的修改能够正常同步到从服务器。

### 补充说明

做了MySQL主从复制以后，使用mysqldump对数据备份时，一定要注意按照如下方式：

```bash
mysqldump –master-data –single-transaction –user=username –password=password dbname> dumpfilename
```

这样就可以保留file和position的信息，在新搭建一个Slave的时候，还原完数据库，file和position的信息也随之更新，接着再start slave 就可以很迅速的完成增量同步。

### 其他复制方式

#### 单一Master和多Slave

由一个Master和多个Slave组成的复制系统比较简单。Slave之间并不互相通信，只能与Master通信。如果写操作较少，读操作很多，可以采用。可以将读操作分布到其他Slave，从而减轻Master的压力。但一旦Slave增加到一定数量时，Slave对Master的负载以及网络带宽都会成为问题。

![MySQL单Master多Slave主从复制原理图](/images/mysql-master-slave-replication-2.png "MySQL One Master Multiple Slave Replication")

#### 单一Master和级联Slave

读操作很多可以采用单一Maste和多Slave，但增大到一定Slave后连到Master的Slave IO线程太多会造成Master压力增大，从而造成数据复制延时。多级复制就是为了解决这个问题。

如果想实现“主-从（主）-从”多级复制，需要设置log-slave-updates参数。同时二进制日志也必须启用。

![MySQL单Master级联Slave主从复制原理图](/images/mysql-master-slave-replication-3.png "MySQL One Master Cascade Slave Replication")

当然，增加复制的级联层次，同一个变更传到最底层的Slave所需要经过的MySQL也会更多，同样可能造成延时较长的风险。如果条件允许，倾向于通过拆分成多个Replication集群来解决。
