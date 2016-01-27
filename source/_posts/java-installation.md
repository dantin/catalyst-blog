title: 安装JDK
date: 2014-10-28 13:59:23
categories: 运维
tags: Java
toc: true
---

本文记录Linux和Mac中安装JDK的步骤。

### 安装准备

下载[Sun JDK](http://www.oracle.com/technetwork/java/javase/downloads/java-se-jdk-7-download-432154.html)

检验操作系统

``` bash
java -version
java version "1.6.0_24"
OpenJDK Runtime Environment (IcedTea6 1.11.1) (rhel-1.45.1.11.1.el6-x86_64)
OpenJDK 64-Bit Server VM (build 20.0-b12, mixed mode)
```

进一步查看JDK信息：

``` bash
rpm -qa | grep java
tzdata-java-2012c-1.el6.noarch
java-1.6.0-openjdk-1.6.0.0-1.45.1.11.1.el6.x86_64
```

__注意：这里也可能是jdk__

``` bash
rpm -qa | grep java
```

卸载OpenJDK：

``` bash
sudo rpm -e --nodeps tzdata-java-2012c-1.el6.noarch
sudo rpm -e --nodeps java-1.6.0-openjdk-1.6.0.0-1.45.1.11.1.el6.x86_64
```

### 安装JDK

#### CentOS

执行以下操作：

``` bash
sudo rpm -ivh jdk-7-linux-x64.rpm
```

__备注：CentOS的JDK默认安装在/usr/java中。__

#### Debian

执行以下操作：

``` bash
sudo tar -zxvf jdk-7u71-linux-x64.tar.gz -C /usr/lib/jvm/
```

__备注：Debian的JDK默认安装在/usr/lib/jvm中。__

恭喜，安装成功！

#### Mac

JDK6之前，Sun并不提供基于OSX的JVM下载，需要从[Sun官网](http://support.apple.com/kb/DL1572?viewlocale=en_US)下载其自定义的安装包。JDK7以后的安装包，可以直接从官网下载。

### 配置环境变量

修改系统环境变量文件`/etc/profile`，追加以下内容：

``` bash
JAVA_HOME=/usr/java/jdk1.7.0
JRE_HOME=/usr/java/jdk1.7.0/jre
PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin
CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib
export JAVA_HOME JRE_HOME PATH CLASSPATH
```

强制修改生效

``` bash
source /etc/profile   //使修改立即生效 
echo $PATH            //查看PATH值
```

### 验证

执行以下操作，查看信息是否正常：

``` bash
java -version
java version "1.7.0"
Java(TM) SE Runtime Environment (build 1.7.0-b147)
Java HotSpot(TM) 64-Bit Server VM (build 21.0-b17, mixed mode)
```

查看系统环境状态

``` bash
echo $PATH
/usr/local/cmake/bin:/usr/lib64/qt-3.3/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/java/jdk1.7.0/bin:/usr/java/jdk1.7.0/jre/bin:/root/bin
```

恭喜，安装成功！