+++
title = "安装Python"
categories = ["Engineering"]
tags = ["Python", "Memo"]
description = "本文记录Python的安装过程"
slug = "python-installation"
date = "2017-01-16T11:32:55+08:00"
+++

### 准备

查看当前系统中的Python版本

```console
python --version
```

返回`Python 2.6.6`为正常。

检查 CentOS 版本

```console
cat /etc/redhat-release
```

返回`CentOS release 6.8 (Final)`为正常。

### 安装

安装所有的开发工具包

```console
yum groupinstall -y "Development tools"
```

安装其它的必需包

```console
yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel
```

下载、编译和安装Python 2.7.13

```console
wget https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz
tar zxf Python-2.7.13.tgz
cd Python-2.7.13
./configure
make && make install
```

默认Python 2.7.13会安装在`/usr/local/bin`目录下。

```console
ll -tr /usr/local/bin/python*

/usr/local/bin/python2.7
/usr/local/bin/python2.7-config
/usr/local/bin/python -> python2
/usr/local/bin/python2 -> python2.7
/usr/local/bin/python2-config -> python2.7-config
/usr/local/bin/python-config -> python2-config
```

而系统自带的Python是在`/usr/bin`目录下。

```console
ll -tr /usr/bin/python*

/usr/bin/python2.6-config
/usr/bin/python2.6
/usr/bin/python
/usr/bin/python2 -> python
/usr/bin/python-config -> python2.6-config
```

更新系统默认Python版本

先把系统默认的旧版Python重命名。

```console
mv /usr/bin/python /usr/bin/python.old
```

删除系统默认的python-config软链接。

```console
rm -f /usr/bin/python-config
```

创建新版本的Python软链接。

```console
ln -s /usr/local/bin/python /usr/bin/python
ln -s /usr/local/bin/python-config /usr/bin/python-config
ln -s /usr/local/include/python2.7/ /usr/include/python2.7
```

以上步骤做完以后，目录`/usr/bin`下的Python应该是

```console
ll -tr /usr/bin/python*

/usr/bin/python2.6-config
/usr/bin/python2.6
/usr/bin/python.old
/usr/bin/python2 -> python
/usr/bin/python -> /usr/local/bin/python
/usr/bin/python-config -> /usr/local/bin/python-config
```

查看新的Python版本

```console
python --version
```

返回`Python 2.7.13`为正常。

### 其他

以下步骤还是有必要的。

为新版Python安装setuptools

```console
wget https://bootstrap.pypa.io/ez_setup.py -O - | python
```

setuptools正确安装完成后，`easy_install`命令就会被安装在`/usr/local/bin`目录下了。

为新版Python安装pip

```console
easy_install pip
```

正确安装完成后，`pip`命令就会被安装在`/usr/local/bin`目录下了。

为新版Python安装distribute包（可选）

```console
pip install distribute
```

至此，新版 Python 即算安装完毕了。


### 更新镜像源

Linux下运行命令

```console
vim ~/.pip/pip.conf
```

然后写入如下内容并保存

```console
[global]
trusted-host =  mirrors.aliyun.com
index-url = http://mirrors.aliyun.com/pypi/simple
```

### 常见错误

`pip`安装包出现错误。

如下：

```console 
...
pgmodule.c:43:20: error: Python.h: No such file or directory
```

解决办法

```console
# CentOS 使用下面命令
# yum install python-devel

```

参考：

* [秋水逸冰的博客](https://teddysun.com/473.html)
