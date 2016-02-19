title: fork, exec和source之间的异同
date: 2016-02-19 10:21:53
categories: 经验分享
tags: OS
toc: true
---

今天，在写脚本时碰到了一个问题，“进程管理supervisor无法停止它管理的进程”。仔细Google了一番，发现原来是自己操作系统的概念模糊，这里记录一下，重点讨论fork，exec，source之间的区别。

### 共同点

作为系统调用，fork、exec、source都能打开一个进程。

### 异同点

那么这三者之间有什么区别呢？

#### fork

用法：

``` bash
/directory/script.sh
```

如果shell中包含执行命令，那么子命令并不影响父级的命令，在子命令执行完后再执行父级命令。子级的环境变量不会影响到父级。

1. fork是最普通的, 就是直接在脚本里面用/directory/script.sh来调用script.sh这个脚本。
2. 运行的时候开一个sub-shell执行调用的脚本，sub-shell执行的时候, parent-shell还在。
3. sub-shell执行完毕后返回parent-shell，sub-shell从parent-shell继承环境变量，但sub-shell中的环境变量不会带回parent-shell。

#### exec

用法：

```bash
exec /directory/script.sh
```

执行子级的命令后，不再执行父级命令。

1. exec与fork不同，不需要新开一个sub-shell来执行被调用的脚本。
2. 被调用的脚本与父脚本在同一个shell内执行。但是使用exec调用一个新脚本以后, 父脚本中exec行之后的内容就不会再执行了。这个情况类似fork进程被“寄生”了。

#### source

用法：

```bash
source /directory/script.sh
```

执行子级命令后继续执行父级命令，同时子级设置的环境变量会影响到父级的环境变量。

1. 与fork的区别是不新开一个sub-shell来执行被调用的脚本，而是在同一个shell中执行. 所以被调用的脚本中声明的变量和环境变量, 都可以在主脚本中得到和使用.

### 使用示例

可以通过下面这两个脚本来体会三种调用方式的不同:

#### 父进程

1.sh

```bash 
#!/bin/bash
A=B
echo "PID for 1.sh before exec/source/fork:$$"
export A
echo "1.sh: \$A is $A"
case $1 in
        exec)
                echo "using exec…"
                exec ./2.sh ;;
        source)
                echo "using source…"
                . ./2.sh ;;
        *)
                echo "using fork by default…"
                ./2.sh ;;
esac
echo "PID for 1.sh after exec/source/fork:$$"
echo "1.sh: \$A is $A"
```

#### 子进程

2.sh

```bash 
#!/bin/bash
echo "PID for 2.sh: $$"
echo "2.sh get \$A=$A from 1.sh"
A=C
export A
echo "2.sh: \$A is $A"
```
 
下面是执行情况：

```bash
$ ./1.sh     
PID for 1.sh before exec/source/fork:5845364
1.sh: $A is B
using fork by default…
PID for 2.sh: 5242940
2.sh get $A=B from 1.sh
2.sh: $A is C
PID for 1.sh after exec/source/fork:5845364
1.sh: $A is B
$ ./1.sh exec
PID for 1.sh before exec/source/fork:5562668
1.sh: $A is B
using exec…
PID for 2.sh: 5562668
2.sh get $A=B from 1.sh
2.sh: $A is C
$ ./1.sh source 
PID for 1.sh before exec/source/fork:5156894
1.sh: $A is B
using source…
PID for 2.sh: 5156894
2.sh get $A=B from 1.sh
2.sh: $A is C
PID for 1.sh after exec/source/fork:5156894
1.sh: $A is C
```

---

摘自：[ChinaUnix](http://blog.chinaunix.net/uid-22548820-id-3181798.html)