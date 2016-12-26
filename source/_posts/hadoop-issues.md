---
title: Hadoop使用问题记录
date: 2016-03-16 09:48:14
categories: 工程
tags: Hadoop
toc: true
---

本文记录使用Hadoop的过程中碰到的问题。

### Name node is in safe mode

#### 重现步骤

测试Hadoop时，碰到Reduce过程中进程卡住，使用`Ctrl+C`退出，再重启Hadoop后，出现异常：

```bash
org.apache.hadoop.dfs.SafeModeException:

    Cannot delete /user/hadoop/output. Name node is in safe mode
```

#### Safe Mode模式

NameNode在启动的时候首先进入安全模式，如果Datanode丢失的block达到一定的比例，则系统会一直处于安全模式状态，即只读状态。

控制参数：`dfs.safemode.threshold.pct`

此值表示HDFS启动时，如果DataNode上报的block个数达到了元数据记录的block个数的0.999倍才可以离开安全模式，否则一直是这种只读模式。如果设为1则HDFS永远是处于SafeMode。

下面这行摘录自NameNode启动时的日志

```bash
The ratio of reported blocks 1.0000 has reached the threshold 0.9990. Safe mode will be turned off automatically in 18 seconds.
```

block上报比例1达到了阀值0.9990。

有两个方法离开这种安全模式

1. 把`dfs.safemode.threshold.pct`设置成一个比较小的值

    缺省值是0.999。

2. 使用命令强制离开

    ```bash
    hadoop dfsadmin -safemode leave
    ```
