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

#### 查看软件信息

```bash
brew info $FORMULA
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

#### 搜索

显示全部可安装的软件清单

```bash
brew search
```

搜索软件

```bash
brew search $FORMULA
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

### 其他

#### 检查Homebrew状态

```bash
brew doctor
```

#### 显示Homebrew版本

```bash
brew -v
```

#### 列出指定版本的依赖关系

```bash
brew deps $FORMULA
```

#### 安装路径

Homebrew自身的安装路径

```bash
brew --prefix
```

FORMULA的安装路径

```bash
brew --prefix $FORMULA
```

### 安装

安装`Command Line Tools`

```bash
xcode-select --install
```

安装Homebrew

```bash
ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"
```

建立Licence

```bash
xcodebuild -license
```

修改环境变量，将$PATH中的`/usr/local/bin/`移至`/usr/bin/`之前。

```bash
vim ~/.bash_profile
export PATH=/usr/local/bin:PATH      # Add This
```

参考

* [Homebrew Requirements](https://github.com/mxcl/homebrew/wiki/Installation)
* [Homebrew Document](https://github.com/Homebrew/homebrew)