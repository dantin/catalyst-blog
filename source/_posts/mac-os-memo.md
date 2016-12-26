---
title: Mac OS备忘录
date: 2016-02-22 13:49:42
categories: 效率
tags: [Mac, OS]
toc: true
---

本文记录Mac OS的常见工具及备忘录。

### 制作启动盘

在苹果商店下载好OS X Mavericks安装文件，然后准备一支16G的USB3.0 U盘。插上U盘，在终端执行：

```bash
sudo /Applications/Install\ OS\ X\ Mavericks.app/Contents/Resources/createinstallmedia --volume /Volumes/untitled --applicationpath /Applications/Install\ OS\ X\ Mavericks.app --nointeraction
```

untitled 是你的u盘盘符，根据实际情况来。

```bash
Erasing Disk: 0%… 10%… 20%… 30%…100%…
>Copying installer files to disk…
Copy complete.
Making disk bootable…
Copying boot files…
>Copy complete.
>Done.
```

看到上面的信息说明启动盘制作成功。

### 隐藏文件开关

显示隐藏文件。

```bash
defaults write com.apple.finder AppleShowAllFiles -boolean true ; killall Finder
```

不显示隐藏文件

```bash
defaults write com.apple.finder AppleShowAllFiles -boolean false ; killall Finde
```

### 远程登录

开启远程登录。

```bash
sudo launchctl load -w /System/Library/LaunchDaemons/ssh.plist
```

关闭远程登录

```bash
sudo launchctl unload -w /System/Library/LaunchDaemons/ssh.plist
```

### 查看依赖

类似Linux中的`ldd`，查看二进制文件的动态链接库依赖。

```bash
otool -L /sbin/ping
```

修改二进制文件动态链接库依赖。

语法

```bash
install_name_tool -change oldname newname input_file
```

例子

```bash
sudo install_name_tool -change /usr/local/lib/libmysqlclient.18.dylib /usr/local/lib/libmysqlclient.20.dylib /Users/david/Documents/venv/python2/lib/python2.7/site-packages/_mysql.so
```

### 开发相关

#### 查看JDK安装

JDK安装路径

```bash
/usr/libexec/java_home -v 1.8
```

