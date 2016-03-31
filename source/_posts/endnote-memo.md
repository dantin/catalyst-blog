title: Endnote备忘录
date: 2016-02-22 13:57:38
categories: 效率
tags: [Software, Endnote, Mac, Windows]
toc: true
---

Endnote是一种文献目录管理软件包。它可以用来创建个人参考文献库，并且可以加入文本、图像、表格和方程式等内容及链接，可以进行当地及远程检索。

### 安装Pages插件

Pages默认不支持Endnote，如需在Pages中增加参考文献支持，需要先[下载](https://support.apple.com/zh-cn/HT204395)Pages插件。

### 安装Endnote

在[Endnote官网](http://www.endnote.com)下载最新版本的Endnote。

_注意_：只有英文版，没有中文版。

当然，也可以直接用`brew cask`安装。

```bash
brew cask install endnote
```

### 破解

#### Endnote X7 for Windows

安装的时候选择30天试用，安装完成之后运行，选择继续试用，然后关闭，知道endnote程序的根目录。

下载授权文件[Licence.dat](http://pan.baidu.com/s/1o6GLgCi)，密码: 9eiy

将此文件直接拷贝到endnote程序根目录下面，即破解成功。

#### Endnote X7 for Mac

同样，在官网下载最新版本的Endnote，安装，选择30天试用，安装成功之后，首先我们要能够看到隐藏文件。

打开“终端”，运行下述命令：

```bash
defaults write com.apple.finder AppleShowAllFiles -boolean true ; killall Finder
```

然后，这样就可以看到隐藏文件了。打开endnote的程序目录（在Finder里面的应用程序里面，找到endnote，击右键选择“在新标签页中打开”或者“显示包文件”），找到.license.dat文件（注意文件开头有一个点），是一个隐藏文件。然后用文本编辑器对它进行编辑。可以看到这个授权文件中是没有内容的。

同样地下载授权文件[Licence.dat](http://pan.baidu.com/s/1o6GLgCi)，密码: 9eiy

同样地，对授权文件通过文本编辑器进行编辑，将授权文件的内容拷贝到上述：.license.dat文件中，并保存。

如果恢复不显示隐藏文件的状态，同样打开“终端”，运行如下命令即可恢复：

```bash
defaults write com.apple.finder AppleShowAllFiles -boolean false ; killall Finder
```

参考

1. [Endnote官网](http://endnote.com/)
2. [Keygen文摘](http://blog.xiaoten.com/crack-endnote-x7-latest-version-of-win-and-mac.html)
