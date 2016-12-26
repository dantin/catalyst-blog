---
title: 安装Hadoop
date: 2016-03-10 15:58:42
categories: 工程
tags: Hadoop
toc: true
---

本文介绍Hadoop的安装过程。

Hadoop允许使用多种模式运行：

* 单机模式
* 伪分布式
* 分布式

这里仅以伪分布模式为例。

### 伪分布式

此模式需要开启本地SSH服务，在本地开启多个JVM进程模拟分布式环境。

#### 开启SSH

在Mac OS X中，使用“系统偏好设置”的“共享”，“远程登录”勾选开启。

当然也可以直接通过命令行[开启远程登录](/2016/02/22/mac-os-memo/)。

```bash
sudo launchctl load -w /System/Library/LaunchDaemons/ssh.plist
```

开启本地SSH登录后，需要将自己的公钥存到公钥保存文件夹中，避免每次执行`ssh localhost`远程登入时都要输入密码。

```bash
ssh-keygen -t dsa -P '' -f ~/.ssh/id_dsa
cat ~/.ssh/id_dsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys
```

#### Homebrew安装

接下来，用Homebrew安装Hadoop。

```bash
brew install hadoop
```

#### 配置Hadoop

Homebrew安装的Hadoop默认路径是：`/usr/local/Cellar/hadoop/2.7.2/libexec`

修改Hadoop环境配置脚本：`$HADOOP_HOME/etc/hadoop/hadoop-env.sh`

```bash
< export HADOOP_OPTS="$HADOOP_OPTS -Djava.net.preferIPv4Stack=true"
---
> # export HADOOP_OPTS="$HADOOP_OPTS -Djava.net.preferIPv4Stack=true"
> export HADOOP_OPTS="$HADOOP_OPTS -Djava.net.preferIPv4Stack=true -Djava.security.krb5.realm= -Djava.security.krb5.kdc="
```

修改`$HADOOP_HOME/etc/hadoop/hadoop-env.sh`

```xml
<configuration>
  <property>
    <name>hadoop.tmp.dir</name>
    <value>/Users/david/Documents/temp/hadoop/hdfs/tmp</value>
    <description>A base for other temporary directories.</description>
  </property>
  <property>
    <!--name>fs.default.name</name-->
    <name>fs.defaultFS</name>
    <!--value>hdfs://localhost:9000</value-->
    <value>hdfs://Davids-MacBook-Pro.local:9000</value>
  </property>
</configuration>
```

这里需要注意hostname，`fs.defaultFS`保存了NameNode的位置，HDFS和MapReduce组件都需要用到它。

修改`$HADOOP_HOME/etc/hadoop/mapred-site.xml.template`

```xml
<configuration>
  <property>
    <name>mapred.job.tracker</name>
    <value>localhost:9010</value>
  </property>
</configuration>
```

修改`$HADOOP_HOME/etc/hadoop/hdfs-site.xml`

```xml
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>
</configuration>
```

变量`dfs.replication`指定了每个HDFS数据库的复制次数。 通常为3，由于我们只有一台主机和一个伪分布式模式的DataNode，将此值修改为1。

### 测试

以下命令的执行路径基于Hadoop的默认路径。(`/usr/local/Cellar/hadoop/2.7.2/libexec`)

#### 启动HDFS

```bash
./sbin/start-dfs.sh
./sbin/stop-dfs.sh
```

#### 启动Yarn

```bash
./sbin/start-yarn.sh
./sbin/stop-yarn.sh
```

执行`./start-dfs.sh`和`./start-yarn.sh`就可以启动Hadoop了。

不过这里会出现一个警告：

```bash
16/03/10 15:24:08 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
```

这对Hadoop的运行没有影响，这个警告和Hadoop 本地库相关，Hadoop本地库只是为了提高效率或者某些不能用Java实现的功能组件库。目前只支持*UNIX，在Mac OS X上没有支持。

#### 格式化HDFS

```bash
hadoop namenode -format
```

#### 示例程序

```bash
$ hadoop jar ../share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.2.jar pi 2 5
```

得到的结果可能是这样的：

```bash
Wrote input for Map #0
Wrote input for Map #1
Starting Job
...
Job Finished in 1.615 seconds
Estimated value of Pi is 3.60000000000000000000
```

可以通过Web端进行监控。

* [Resource Manager](http://localhost:50070)
* [JobTracker](http://localhost:8088)
* [Specific Node Information](http://localhost:8042)

通过他们可以访问 HDFS filesystem, 也可以取得结果输出文件.

参考

1. [Hadoop官网中Pseudo Distributed Node安装](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html#Pseudo-Distributed_Operation)
2. [Hadoop Yarn介绍](http://www.uml.org.cn/sjjm/201302251.asp)
3. [Linux中的Hadoop安装](http://blog.csdn.net/ggz631047367/article/details/42426391)
