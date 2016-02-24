title: Linux备忘录
date: 2014-10-29 07:26:53
categories: 学习
tags: Linux
toc: true
---

本文记载了在Linux使用中经常碰到的一些概念和使用方法。

### 环境变量

一些特殊变量会被Shell环境和操作系统环境存储特别的值，称之为__环境变量__。

环境变量泛指那些未在当前进程中定义，而从父进程中继承而来的变量。

#### 设置环境变量

如，设置代理服务器：

``` bash
HTTP_PROXY=http://192.168.0.2:3128
export HTTP_PROXY
```

#### 查看环境变量

``` bash
env
```

#### 查看进程环境变量

``` bash
cat /proc/$PID/environ
```

环境变量以名值对方式显示，用`null`字符分割。

若需人性化显示，使用`tr`命令。

``` bash
cat /proc/$PID/environ | tr '\0' '\n'
```

#### 常用环境变量

##### PATH

可执行文件的搜索路径。

`$PATH`通常定义在`/etc/environment`，`/etc/profile`或`~/.bashrc`中

增加搜索路径的修改方式

``` bash
# 方法一
export PATH="$PATH:/home/user/bin"
# 方法二
PATH="$PATH:/home/user/bin"
export PATH
```

##### SHELL

判断使用的是哪种SHELL

``` bash
echo $SHELL
```

##### UID

登录用户的ID

检查当前脚本是否以超级用户登录

``` bash
if [ $UID -ne 0 ]; then
    echo "Non root user. Please run as root."
else
    echo "Root User"
fi
```

##### PS1

Bash的提示字符串，通常设置于`~/.bashrc`，如：

``` bash
PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
```

* `\u`，扩展为用户名
* `\h`，扩展为主机名
* `\w`，扩展为当前工作目录

### 命令

#### 终端打印

##### echo

显示打印的内容，每次调用后会添加一个换行符。

* 不使用引号的`echo`不能在显示文本中使用`;`
* 单引号的`echo`不会对变量（`$var`）转义
* 双引号的`echo`内不能再打`"`

__注意：转义特殊字符需要在`echo`前使用`set +H`__

##### printf

`printf "formater string" variables`

可以使用格式化字符串，必须手动添加换行符。

* `%s`，字符串
* `%c`，字符
* `%d`，整数
* `%f`，浮点数
* `\n`，换行

如：`%-4.2f`，左对齐，保留两位小数

### 进程

#### 根据应用名找进程ID

##### pgrep

``` bash
pgrep vim
```

#### 结束进程

命令：`killall <process name>`

常用于直接结束掉相关进程。如：重启ftpd时进程没有完全退出，导致重启失败

``` bash
sudo killall pure-ftpd
```

所有pure-ftpd相关进程都会被结束掉。

### 文件系统

#### 文件

##### 链接文件

创建软链接文件

``` bash
ln -s <source file> <target symbolic link file>
# example: ln  -s  /lib/lsb   /usr/lj
# 在usr目录下建立指向/lib/lsb目录的lj文件。
```

-s 是 symbolic的意思。

### 网络

#### 端口相关

在使用Linux系统的过程中，有时候会遇到端口被占用而导致服务无法启动的情况。比如HTTP使用80端口，但当启动Apache时，却发现此端口正在使用。

这种情况大多数是由于软件冲突、或者默认端口设置不正确导致的，此时需要查看究竟哪个进程占用了端口，来决定进一步的处理方法。

##### 查看端口使用

命令：`lsof -i`

``` bash
lsof -i
COMMAND PID USER FD TYPE DEVICE SIZE NODE NAME
nginx 2333 root 6u IPv4 6242 TCP *:http (LISTEN)
nginx 2334 www 6u IPv4 6242 TCP *:http (LISTEN)
sshd 2349 root 3u IPv6 6283 TCP *:ndmp (LISTEN)
sshd 2349 root 4u IPv6 6286 TCP *:ssh (LISTEN)
```

返回结果概述：
* 第一段是进程名称
* 最后一列是侦听的协议、侦听的IP与端口号、状态。如果端口号是已知的常用服务（如80、21等），则会直接显示协议名称，如http、ftp、ssh等。

##### 查看某一端口的占用情况

命令：`lsof -i:<port number>`

``` bash
lsof -i:21
COMMAND PID USER FD TYPE DEVICE SIZE NODE NAME
pure-ftpd 2651 root 4u IPv4 7047 TCP *:ftp (LISTEN)
pure-ftpd 2651 root 5u IPv6 7048 TCP *:ftp (LISTEN)
```

这里显示出21号端口正在被pure-ftpd使用，状态是listen。

### 文件

#### 目录

拷贝一个目录

``` bash
cp -r <source directory> <destination directory>
```

#### 常用文件类型

##### rpm.bin

rpm的压缩文件。如：Sun官网下载的jdk-6u45-linux-x64-rpm.bin。

使用方法：

``` bash
./jdk-6u45-linux-x64-rpm.bin
```

执行后得到一个rpm文件，如：jdk-6u45-linux-x64.rpm

##### rpm

RedHat/CentOS的安装包。如：JDK的安装包jdk-6u45-linux-x64.rpm

使用方法：

``` bash
rpm -ivh jdk-6u45-linux-x64.rpm
```

执行结果：将对于软件安装到系统。

##### gz

解压：

``` bash
tar -zxvf file.tar.gz
```

创建：

``` bash
tar -cvf file.tar <file or directory>
```

##### bz2

bzip2是一个压缩能力更强的压缩程序，.bz2结尾的文件就是bzip2压缩的结果。

解压：

``` bash
tar -jxvf file.tar.bz2
```

##### xz

解压：

``` bash
# 将 xxx.tar.xz解压成 xxx.tar
xz -d xxx.tar.xz
tar xvf xxx.tar
```

创建：

``` bash
tar cvf xxx.tar <file or directory>
xz -z xxx.tar
```

##### tar

不解压文件，看文件内容

```bash
tar -tvzf *.tar.gz
```
