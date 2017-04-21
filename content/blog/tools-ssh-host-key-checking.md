+++
date = "2017-04-21T10:35:09+08:00"
slug = "tools-ssh-host-key-checking"
title = "禁用SSH远程主机的公钥检查"
categories = ["Misc"]
tags = ["Tools", "Memo"]
description = "本文记录SSH公钥检查的安全机制"
+++

SSH公钥检查是一个重要的安全机制，可以防范中间人劫持等黑客攻击。但是在特定情况下，严格的SSH公钥检查会破坏一些依赖SSH协议的自动化任务，就需要一种手段能够绕过SSH的公钥检查。

### 什么是SSH公钥检查

SSH连接远程主机时，会检查主机的公钥。如果是第一次该主机，会显示该主机的公钥摘要，提示用户是否信任该主机：

```console
The authenticity of host '192.168.0.110 (192.168.0.110)' can't be established.
RSA key fingerprint is a3:ca:ad:95:a1:45:d2:57:3a:e9:e7:75:a8:4c:1f:9f.
Are you sure you want to continue connecting (yes/no)?
```

当选择接受，就会将该主机的公钥追加到文件`~/.ssh/known_hosts`中。当再次连接该主机时，就不会再提示该问题了。 如果因为某种原因（服务器系统重装，服务器间IP地址交换，DHCP，虚拟机重建，中间人劫持），该IP地址的公钥改变了，当使用SSH连接的时候，会报错：

```console
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that the RSA host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
e9:0c:36:89:7f:3c:07:71:09:5a:9f:28:8c:44:e9:05.
Please contact your system administrator.
Add correct host key in /Users/david/.ssh/known_hosts to get rid of this message.
Offending key in /Users/david/.ssh/known_hosts:81
RSA host key for 192.168.0.110 has changed and you have requested strict checking.
Host key verification failed.
```

上面的警告信息说的是：

服务器公钥已经改变，新的公钥的摘要是：`e9:0c:36:89:7f:3c:07:71:09:5a:9f:28:8c:44:e9:05`

该服务器原来的公钥记录在文件 ~/.ssh/known_hosts 中第`81`行。

如果确认不是中间人劫持，需要连接到该服务器，怎么办呢？最简单的就是用`vim`打开`~/.ssh/known_hosts`文件，定位到`81`行，将该行删除。之后就可以使用`ssh`连接了。

如何让连接新主机时，不进行公钥确认？

在首次连接服务器时，会弹出公钥确认的提示。这会导致某些自动化任务，由于初次连接服务器而导致自动化任务中断。或者由于`~/.ssh/known_hosts`文件内容清空，导致自动化任务中断。SSH客户端的`StrictHostKeyChecking`配置指令，可以实现当第一次连接服务器时，自动接受新的公钥。只需要修改`/etc/ssh/ssh_config`文件，包含下列语句：

```bash
Host *
 StrictHostKeyChecking no
```

或者在`ssh`命令行中用`-o`参数

```bash
ssh  -o StrictHostKeyChecking=no  192.168.0.110
```

### 如何防止远程主机公钥改变导致SSH连接失败

当确认中间人劫持攻击风险比较小的情况下，才可以使用下面的方法，禁用SSH远程主机的公钥检查。SSH客户端提供一个`UserKnownHostsFile`配置，允许指定不同的`known_hosts`文件。那么将`known_hosts`指向不同的文件，不就不会造成公钥冲突导致的中断了么？

```bash
ssh -o UserKnownHostsFile=/dev/null 192.168.0.110

The authenticity of host '192.168.0.110 (192.168.0.110)' can't be established.
RSA key fingerprint is e9:0c:36:89:7f:3c:07:71:09:5a:9f:28:8c:44:e9:05.
Are you sure you want to continue connecting (yes/no)?
```

提示信息由公钥改变中断警告，变成了首次连接的提示。和之前提到的`StrictHostKeyChecking`配置配合使用，则不再有任何警告出现了：

```bash
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null 192.168.0.110

Warning: Permanently added '192.168.0.110' (RSA) to the list of known hosts.
david@192.168.0.110's password:
```

如果设置了无口令SSH登录（即通过客户端公钥认证），就可以直接连接到远程主机。这是基于SSH协议的自动化任务常用的手段。
