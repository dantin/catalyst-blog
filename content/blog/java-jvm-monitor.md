+++
date = "2016-06-12T09:56:34+08:00"
title = "深入理解Java虚拟机之六：性能监控工具"
categories = ["Scholar"]
tags = ["Java", "JVM"]
description = "本文记录JDK自带的性能监控工具"
slug = "java-jvm-monitor"
+++

JDK的bin中提供了许多的工具，来用于虚拟机的监控。

### 命令行工具

#### jps

显示虚拟机中的所有Java进程情况。

默认会显示该进程执行主类函数所在的类以及进程的本地虚拟机唯一ID（LVMID）。参数：

* -q：只输出LVMID 
* -m：输出进程启动时的main参数 
* -l：输出主类的全名，如果进程执行的是jar包，输出Jar路径 
* -v：输出虚拟机进程启动时的JVM参数

如：

```bash
jps -l
25330 sun.tools.jps.Jps
25296
 
jps -lv
25356 sun.tools.jps.Jps -Dapplication.home=/Library/Java/JavaVirtualMachines/jdk1.7.0_71.jdk/Contents/Home -Xms8m
25296  -Dosgi.requiredJavaVersion=1.6 -XstartOnFirstThread -Dorg.<span class="wp_keywordlink"><a href="http://res.importnew.com/eclipse" title="Eclipse ImportNew主页" target="_blank">Eclipse</a></span>.swt.internal.carbon.smallFonts -XX:MaxPermSize=256m -Xms40m -Xmx512m -Xdock:icon=../Resources/Eclipse.icns -XstartOnFirstThread -Dorg.eclipse.swt.internal.carbon.smallFonts
```

#### jstat

显示本地或者远程虚拟机进程中的类加载、内存、垃圾收集、JIT编译等运行参数，格式为：

```bash 
jstat [option vmid [interval[s|ms] [count]]] 
```

* vmid表示本地的进程ID就是LVMID，但是远程的话格式为：\[protocol:\]\[//\]lvmid\[:port\]/servername 
* interval和count表示查询间隔和次数, jstat -gc 2764 250 20表示查询2764进程的垃圾回收每250ms一次共查询20次 
* option表示需要查看的内容： 
    * -class：类装置、卸载数量、总量以及类装载消耗的时间
    * -gc：监视Java堆状况，包括eden区、两个survivor区、年老代、永久代等的容量、已用空间、gc时间合计等
    * -gccapacity：内容与-gc基本相同，输出主要关注Java堆各个区使用到的最大、最小空间
    * -gcutil：内容与-gc基本相同，关注已使用区域占总空间的百分比
    * -gccause：内容与-gcutil一样，并且多输出导致上一次gc产生的原因
    * -gcnew：新生代的情况 
    * -compiler：输出JIT编译器编译过的方法、耗时等信息

如：查询 25296 进程的虚拟机状况，并且每隔 1000 毫秒一次，显示 5 次。

```bash
jstat -gcutil 25296 1000 5
  S0     S1     E      O      P     YGC     YGCT    FGC    FGCT     GCT
  0.00  99.54  90.43  93.70  95.23     55    1.156     5    1.990    3.146
  0.00  99.54  90.43  93.70  95.23     55    1.156     5    1.990    3.146
  0.00  99.54  90.43  93.70  95.23     55    1.156     5    1.990    3.146
  0.00  99.54  90.43  93.70  95.23     55    1.156     5    1.990    3.146
  0.00  99.54  90.43  93.70  95.23     55    1.156     5    1.990    3.146
```

#### jinfo

显示和调整虚拟机的各项参数，格式：

```bash 
jinfo [option] pid 
```

* -v：查看虚拟机启动时指定的参数列表 
* -flag：查询某个参数的情况

```bash
jinfo -flag CMSInitiatingOccupancyFraction
```

#### jmap

生成内存印象快照，还可以查看finalize队列情况，Java堆和永久代的情况，如空间使用率和当前用的是哪种收集器等。

格式：

```bash
jmap [option] vmid
jmap -heap:format=b <process-id>
```

* -dump 转为dump 
* -finalizerinfo finalize队列情况 
* -heap 堆的详细情况 
* -histo 对中对象统计信息 
* -permstat 永久代内存情况，只有在Linux和Solaris平台下有用

#### jhat

快照分析，配合jmap使用，会在7000端口开启http服务，在网页上查看信息。

一般不使用这个命令来分析，会使用专业的工具来分析 dump 文件，如：Eclipse memory analyzer等。

#### jstack

堆栈跟踪，生成当时时刻的线程快照，格式：

```bash
jstack [option] vmid 
```

* -F 当输出请求不被响应时强制输出线程堆栈 
* -l 除线程为显示锁的信息 
* -m 如果调用了本地方法的话，显示c/C++堆栈

#### HSDIS JIT反汇编

可以使用HSDIS来进行打印汇编情况，具体需查资料。

### 可视化工具

#### Jconsole

JConsole基于JMX的可视化监视工具，在bin下的jconsole执行，会自动搜索所有的java进程

#### VisualVM

最为强大的监控工具，包含：

* 故障处理
* 显示虚拟机的进程和配置 
* dump和分析 

备注：要使用VisualVM的话首先要去安装插件，在工具->插件中安装。
