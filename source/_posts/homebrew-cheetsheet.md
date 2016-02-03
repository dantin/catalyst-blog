title: Homebrew Cheetsheet
date: 2016-01-19 10:33:58
categories: 经验分享
tags: [Homebrew, Cheetsheet]
toc: true
---

本文记录Homebrew的常用方法。

### 查看相关

#### 查看过期的软件

```bash
brew outdated
```

#### 查看安装的软件

```bash
brew list
```

### 更新相关

#### 更新Homebrew

```bash
brew update
```

#### 更新所有软件

```bash
brew upgrade
```

#### 更新特定软件

```bash
brew upgrade $FORMULA
```

### 释放空间


默认情况下，Homebrew不会卸载任何版本的空间，因此需要手动清理。

#### 清理某一软件

```bash
brew cleanup $FORMULA
```

#### 清理所有软件

```bash
brew cleanup
```

#### 查看所有可清理软件

```bash
brew cleanup -n
```
