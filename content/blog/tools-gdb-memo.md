+++
date = "2017-08-22T22:41:11+08:00"
title = "GDB备忘录"
categories = ["Misc"]
tags = ["Memo", "GDB"]
description = "本文记录GDB命令的常见用法"
slug = "tools-gdb-memo"
+++

### 安装

```console
brew install gdb
```

### 开启调试编译选项

希望gdb调试时输出行号与堆栈等详细信息需要gcc编译的时候使用-g选项

```console
gcc -o test -g -rdynamic test.c
```

__注意__：`homebrew`安装的`gnu`版本的`gcc`在`macox`上不支持`-rdynamic`选项，此处使用的是`xcode`提供的`gcc`。

### 调试

```console
gdb test

gdb>run
....
The GDB command:
„-exec-run“ returned the error:
„,msg=„Unable to find Mach task port for process-id 62593:
(os/kern) failure (0x5). (please check gdb is codesigned - see taskgated(8))““
```

不出意外将会遇到上述错误。这是由于`MacOS`的安全策略，`homebrew`安装的`gdb`没有签名导致。

### 签名gdb

1. 打开 “钥匙串访问”，位于`/Applications/Utilities/Keychain Access.app`
2. 打开菜单 / 钥匙串访问 / 证书助理 / 创建证书
3. 在”创建您的证书”窗口设置如下
   * 名称: gdbc
   * 身份类型: 自签名根证书
   * 证书类型: 代码签名
   *勾选”让我覆盖这些默认值”
4. 点击”继续”，将”有效期（天数）”设置为: 3650
5. 点击若干次”继续”，指导出现”指定用于该证书的位置””
   * 钥匙串: 系统
6. 点击”创建”，会弹出用户名密码输入框，输入密码，点击”修改钥匙串”
7. 在“系统”钥匙串找到刚才创建的”gdbc”证书，右键”显示简介”，在“信任”分类下找到“代码签名”，指定为“总是信任”。
8. 退出“钥匙串访问”

要让刚刚添加的证书生效需要重启`taskgated`服务或者重启系统

```console
sudo killall taskgated
```

证书准备好了，接下来给`gdb`签名

```console
codesign -fs gdbc /usr/local/bin/gdb
```

### lldb

即使给签名`gdb`以后，在执行`gdb`调试仍然无法显示行号（行号显示为 ??），新版本的`Macosx`已经和`gdb`不兼容了，`lldb`是`gdb`的替代者。使用`lldb`调试可以显示错误发生位置的行号。

参考：

* [How to install and codesign GDB on OS X El Capitan](https://medium.com/@royalstream/how-to-install-and-codesign-gdb-on-os-x-el-capitan-aab3d1172e95)
* [Gist](https://gist.github.com/hlissner/898b7dfc0a3b63824a70e15cd0180154)
