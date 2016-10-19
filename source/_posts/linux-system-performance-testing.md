---
title: Linux性能测试
date: 2016-10-17 16:02:50
categories: 工程
tags: Linux
toc: true
---

本文记录Linux性能测试方法。

### CPU相关

测试方式：通过bc命令计算圆周率

```
echo "scale=5000;4*a(1)" | bc -l -q
```

参数含义：

```
-l --mathlib: 使用标准数学库
```

### 硬盘相关

测试方式：使用dd指令，对磁盘进行连续写入，不使用内存缓冲区，每次写入8k的数据，总共写入20万次，产生1.6G大小的文件。

```
dd if=/dev/zero of=/data01/test.dbf bs=8k count=200000 conv=fdatasync
```

参数含义：

```
bs=<字节数>: 将ibs( 输入)与obs(输出)设成指定的字节数。
cbs=<字节数>: 转换时，每次只转换指定的字节数。
conv=<关键字>: 指定文件转换的方式。
count=<区块数>: 仅读取指定的区块数。
ibs=<字节数>: 每次读取的字节数。
if=<文件>: 从文件读取。
obs=<字节数>: 每次输出的字节数。
of=<文件>: 输出到文件。
seek=<区块数>: 一开始输出时，跳过指定的区块数。
skip=<区块数>: 一开始读取时，跳过指定的区块数。
```

conv参数的意义：

* sync函数只是将所有修改过的块缓冲区排入写队列，然后就返回，它并不等待实际写磁盘操作结束。通常称为update的系统守护进程会周期性地（一般每隔30秒）调用sync函数。这就保证了定期冲洗内核的块缓冲区。命令sync(1)也调用sync函数。
* fsync函数只对由文件描述符filedes指定的单一文件起作用，并且等待写磁盘操作结束，然后返回。fsync可用于数据库这样的应用程序，这种应用程序需要确保将修改过的块立即写到磁盘上。
* fdatasync函数类似于fsync，但它只影响文件的数据部分。而除数据外，fsync还会同步更新文件的属性。

### 网卡相关

网络测试拷贝包，测试网卡吞吐量。

``` bash
ftp -n <hostname> <<!
user <username> <password>
bin
prom
put "|dd if=/dev/zero bs=1m" /dev/null
by
!
```

运行该脚本，通过查看系统的网络信息查看网络最大吞吐量。

```
prom: Toggle interactive mode for downloads
```
