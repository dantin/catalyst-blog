title: Mac OS备忘录
date: 2016-02-22 13:49:42
categories: 学习
tags: [Mac, OS]
toc: true
---

本文记录Mac OS的常见工具及备忘录。

### 隐藏文件开关

显示隐藏文件。

```bash
defaults write com.apple.finder AppleShowAllFiles -boolean true ; killall Finder
```

不显示隐藏文件

```bash
defaults write com.apple.finder AppleShowAllFiles -boolean false ; killall Finde
```
