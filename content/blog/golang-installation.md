+++
date = "2016-09-13T11:07:45+08:00"
title = "Golang安装"
categories = ["Engineering"]
tags = ["Golang"]
description = "本文记录Golang的安装过程"
slug = "golang-installation"
+++

本文记录Mac中安装Golang环境的步骤。

### 使用brew

使用brew安装最方便。

```bash
brew install go
....

As of go 1.2, a valid GOPATH is required to use the `go get` command:
  https://golang.org/doc/code.html#GOPATH

You may wish to add the GOROOT-based install location to your PATH:
  export PATH=$PATH:/usr/local/opt/go/libexec/bin
```

### 设置路径

使用Go需要GOPATH和GOROOT，设置如下：

```bash
cat ~/.zshrc
# go
export GOROOT=/usr/local/opt/go/libexec
export GOPATH=$HOME/.go
export PATH=$PATH:$GOROOT/bin:$GOPATH/bin
```

GOPATH和GOROOT的安装因人而异，选择自己喜欢的方式。

### 测试

创建一个Hello World的小程序。

```bash
cd ~/workspace
vi hello.go
```

代码如下：

```go
// hello.go
package main
import "fmt"

func main() {
  fmt.Printf("Hello, world!")
}
```

运行

```bash
go run hello.go
Hello, world!%
```

安装成功！

参考

[Go安装文档](https://golang.org/doc/install)
