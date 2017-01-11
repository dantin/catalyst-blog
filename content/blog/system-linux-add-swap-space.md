+++
date = "2017-01-05T17:28:22+08:00"
title = "为Linux增加SWAP空间"
categories = ["Engineering"]
tags = ["Linux"]
description = "本文介绍如何为Linux增加Swap空间"
slug = "system-linux-add-swap-space"
+++

本文记录利用Swap File增加虚拟内存的过程。

### 检查

查看系统是否配置了交换区域。

```console
sudo swapon -s
```

没有的话，直接开始创建Swap File。

创建一个1G的文件。

```console
sudo fallocate -l 1G /swapfile
# 确认是否是自己所需要的文件大小
ls -lh /swapfile
```

### 启用Swap文件

调整文件的权限，

```console
# 若该文件能被其他用户随意的读写，则会产生很大的安全隐患。
sudo chmod 600 /swapfile
# 让系统开始设置交换区域
sudo mkswap /swapfile
# 启用该文件
sudo swapon /swapfile
```

现在基本的步骤已经完成了，可以使用最初的命令验证swap file是否正确使用。

```console
sudo swapon -s
Filename                    Type          Size     Used     Priority
/swapfile                               file          1048572     0     -1
```

交换分区已经成功设置，系统会在必要的时候使用它。

__注意__：现在已经启用了swap文件，但当系统重启时，不会自动地启用该swap文件。可以通过修改fstab文件实现开机使用swap文件。

### 启动时加载

用root权限编辑

```console
sudo vim /etc/fstab
```

在文件的最后，需要添加一行告诉操作系统自动使用swap文件。

```console
/swapfile   none    swap    sw    0   0
```
