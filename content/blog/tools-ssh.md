+++
date = "2016-04-20T11:18:26+08:00"
title = "SSH备忘录"
categories = ["Misc"]
tags = ["Tools", "Memo"]
description = "本文记录如何优雅地使用SSH"
slug = "tools-ssh"
+++

本文记录如何优雅地使用SSH。

### 证书登录

作为一个开发者，经常要面对管理一大堆服务器的情况，对UNIX类服务器，一般使用SSH连接来管理。下文介绍使用证书来登陆的办法。

使用证书的好处如下：

* 安全，目前生成证书的方式不管是RSA还是DSA无论从位数上还是加密方式上都比自己生成的密码安全许多。
* 方便，有了证书以后你就不用再记忆密码了，系统会自动使用证书跟服务器接驳，这一过程不需要人工干预使用证书连接ssh也非常简单。

首先生成一个证书，在服务器Shell中输入如下命令：

```bash
ssh-keygen -t rsa -C <comment> -f my-key-file
```

* -t：定义的是加密方式，一般有rsa和dsa两种。
* -C：定义的是注释，一般也可以不写。
* -f：定义了输出的证书文件名，不需要写后缀，因为生成的证书包含了公钥和私钥两个文件，它会自动帮你加文件名。

执行后结果如下：

```bash
ssh-keygen -t rsa -C test -f my-key-file
Generating public/private rsa key pair.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in my-key-file.
Your public key has been saved in my-key-file.pub.
The key fingerprint is:
57:75:20:37:e2:53:29:ef:86:09:8e:1b:47:2b:6f:88 test
The key's randomart image is:
+--[ RSA 2048]----+
|            o *o.|
|           ..*.o |
|            +o   |
|          o. ..  |
|        S+.o +   |
|        +.+ o o  |
|       . B   .   |
|      E o o      |
|         .       |
+-----------------+
$ ls
my-key-file     my-key-file.pub
```

执行完成后得到两个文件`my-key-file`和`my-key-file.pub`。前者是私钥，后者是公钥。

现在，把公钥文件上传到服务器上。

```bash
scp my-key-file.pub loginname@yourdomain.com:.
```

接下来告诉服务器，以后处理loginname的登录时用公钥来验证。执行如下命令

```bash
cat my-key-file.pub >> ~/.ssh/authorized_keys
```

__注意：如果authorized_keys 不为 600的话，ssh就登录不上去。即使所有的配置都正确。__

确保目录及文件的权限：

```bash
chmod 700 ~/.ssh/
chmod 600 authorized_keys
```

用密钥的方式连接服务器是需要服务器上的SSH支持，需要SSH的配置文件(默认是在/etc/ssh/sshd_config)里的PubkeyAuthentication设置为yes。

退出ssh连接，回到本地。将刚才生成的my-key-file文件拷贝到~/.ssh目录下。

编辑~/.ssh/config文件，如果没有，就创建一个，在其中写入如下配置内容：

```bash
Host yourdomain.com
     IdentityFile ~/.ssh/my-key-file
```

现在，就可以正常登录服务器了，第一次登录会出现：

```bash
ssh loginname@yourdomain.com
The authenticity of host 'yourdomain.com (xxx.xxx.xxx.xxx)' can't be established.
RSA key fingerprint is xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx.
Are you sure you want to continue connecting (yes/no)?
```

输入yes即可完成登录。
