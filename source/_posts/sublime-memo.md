---
title: Sublime备忘录
date: 2016-08-09 18:01:53
categories: 效率
tags: [Mac]
toc: true
---

Sublime是Mac下的文字编辑器，本文记录其常见用法。

### 安装Package Control

Package Control是一个用来进行在线安装插件的工具，在使用前需要先安装。

点击菜单中的 “View”–“Show Console”（也可通过快捷键 Ctrl + ` 打开，不过可能因与系统其他软件快捷键冲突而打不开）调出 Console。然后把[官方的代码](https://packagecontrol.io/installation#st3)粘贴进去后回车即可，需稍微等待一段时间。

重启Sublime Text即可。

### 常用插件

使用`Cmd + Shift + P`调出面板，然后输入`pci`，选中“Package Control: Install Package”并回车，然后通过输入插件的名字找到插件并回车安装即可。

#### AStyleFormatter

Sublime Text 3下的C/C++代码整理工具，好像还支持java。

在新弹出的窗口中输入AStyleFormatter，点击它便开始自动下载安装。

使用时只要在代码编辑页面右击，选择AStyleFormatter->Format即可，快捷键为Ctrl+Alt+F。

### 快捷键

#### 跳转类

```bash
Alt+PageUp   文件首
Alt+PageDown 文件尾
Ctrl+G       跳到第几行
```

#### 显示类

```bash
Ctrl+Tab 按文件浏览过的顺序，切换当前窗口的标签页。
Cmd+Alt+1 一屏显示
Cmd+Alt+2 二屏显示
```