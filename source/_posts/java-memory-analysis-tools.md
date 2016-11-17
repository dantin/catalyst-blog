---
title: Java内存分析工具
date: 2016-11-17 11:24:36
categories: 工程
tags: Java
toc: true
---

生产环境中，尤其是吃大内存的JVM，一旦出现内存泄露等问题是非常容易引发OutofMemory的，如果没有一个好的工具提供给开发人员定位问题和分析问题，那么这将会是一场噩梦。

目前JDK其实自带有一些内存泄露分析工具专门用于帮助开发人员定位内存泄露等问题，相关问题的定位办法。

### 堆转储

jmap是JDK自带的一种用于生成内存镜像文件的工具，通过该工具，开发人员可以快速生成dump文件。开发人员可以使用命令“jmap -help”查看jmap的常用命令。

命令格式

```bash
jmap [ option ] pid
jmap [ option ] executable core
jmap [ option ] [server-id@]remote-hostname-or-IP
```

参数说明

1. options： 
    `executable`：可产生core dump的java可执行程序
    `core`：将被打印信息的core dump文件
    `remote-hostname-or-IP`：远程debug服务的主机名或ip
    `server-id`：唯一id,假如一台主机上多个远程debug服务 
2. 基本参数：
    `-dump:[live,]format=b,file=<filename>`：使用hprof二进制形式，输出jvm的heap内容到文件。live子选项是可选的，假如指定live选项，那么只输出活的对象到文件；
    `-finalizerinfo`：打印正等候回收的对象的信息；
    `-heap`：打印heap的概要信息，GC使用的算法，heap的配置及wise heap的使用情况；
    `-histo[:live]`：打印每个class的实例数目、内存占用、类全名信息。JVM的内部类名字开头会加上前缀”*”。如果live子参数加上后，只统计活的对象数量；
    `-permstat`：打印classload和JVM heap永久代的信息，包含每个classloader的名字、活泼性、地址、父classloader和加载的class数量。另外，内部String的数量和占用内存数也会打印出来；
    `-F`：强制在pid没有相应的时候使用-dump或者-histo参数。在这个模式下live子参数无效；
    `-h | -help`：打印辅助信息；
    `-J`：传递参数给jmap启动的JVM

### 使用示例

64位机上使用需要使用如下方式：

```bash
jmap -J-d64 -heap pid
```

#### 查询JVM堆的概要信息

```bash
jmap -heap 9142

Attaching to process ID 9142, please wait...
Debugger attached successfully.
Server compiler detected.
JVM version is 20.10-b01

using thread-local object allocation.
Parallel GC with 4 thread(s)

Heap Configuration:
   MinHeapFreeRatio = 40
   MaxHeapFreeRatio = 70
   MaxHeapSize      = 1031798784 (984.0MB)
   NewSize          = 1048576 (1.0MB)
   MaxNewSize       = 4294901760 (4095.9375MB)
   OldSize          = 4194304 (4.0MB)
   NewRatio         = 2
   SurvivorRatio    = 8
   PermSize         = 16777216 (16.0MB)
   MaxPermSize      = 67108864 (64.0MB)

Heap Usage:
PS Young Generation
Eden Space:
   capacity = 16121856 (15.375MB)
   used     = 15074368 (14.37603759765625MB)
   free     = 1047488 (0.99896240234375MB)
   93.50268356199187% used
From Space:
   capacity = 2686976 (2.5625MB)
   used     = 2684584 (2.5602188110351562MB)
   free     = 2392 (0.00228118896484375MB)
   99.91097799161585% used
To Space:
   capacity = 2686976 (2.5625MB)
   used     = 0 (0.0MB)
   free     = 2686976 (2.5625MB)
   0.0% used
PS Old Generation
   capacity = 42991616 (41.0MB)
   used     = 5071824 (4.8368682861328125MB)
   free     = 37919792 (36.16313171386719MB)
   11.797239722275153% used
PS Perm Generation
   capacity = 16777216 (16.0MB)
   used     = 11304456 (10.780769348144531MB)
   free     = 5472760 (5.219230651855469MB)
   67.37980842590332% used
```

#### Dump jvm内存信息

```bash
jmap -F -dump:format=b,file=tomcat.bin 9142
Attaching to process ID 9142, please wait...
Debugger attached successfully.
Server compiler detected.
JVM version is 20.10-b01
Dumping heap to tomcat.bin ...
Finding object size using Printezis bits and skipping over...
Heap dump file created
```

### 使用工具进行内存泄露分析

常见工具如Eclipse的[MAT工具](http://www.eclipse.org/mat/downloads.php)，或者是JDK自带的jhat。

如先准备一段测试代码，如下所示：

```java
/** 
 * java -server -Xms1024m -Xmx1024m -Xmn384m -XX:+UseParallelOldGC 
 * -XX:+PrintGCApplicationStoppedTime -XX:+PrintGCDateStamps -XX:+PrintGCDetails 
 * -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=<path>/heap.bin GCTest
 */
public class GCTest {

    public static void main(String[] args) {
        final int _1mb = 1024 * 1024;
        byte[] value1 = new byte[_1mb * 100];
        byte[] value2 = new byte[_1mb * 100];
        byte[] value3 = new byte[_1mb * 100];
        new Thread() {
            public void run() {
                byte[] value4 = new byte[_1mb * 400];
            }
        } .start();
        byte[] value5 = new byte[_1mb * 200];
    }
}
```

选项“-XX:+HeapDumpOnOutOfMemoryError ”和-“XX:HeapDumpPath”所代表的含义就是当程序出现OutofMemory时，将会在相应的目录下生成一份dump文件，而如果不指定选项“XX:HeapDumpPath”则在当前目录下生成dump文件。

#### MAT

当上述程序执行时，必然会触发OutofMemory，然后在所指定的目录下找到生成的dump文件后，我们便可以通过MAT工具来进行分析了。当成功启动MAT后，通过菜单选项“File->Open heap dump...”打开指定的dump文件后，将会生成Overview选项。

在Overview选项中，以饼状图的形式列举出了程序内存消耗的一些基本信息，其中每一种不同颜色的饼块都代表了不同比例的内存消耗情况。如果说需要定位内存泄露的代码点，我们可以通过Dominator Tree菜单选项来进行排查(MAT工具仅仅只是一个辅助，分析OutofMemory并不存在一个固定的方式和准则，因此仔细观察和分析才能够找到问题所在)

#### jhat

jhat是用来分析java堆的命令，可以将堆中的对象以html的形式显示出来，包括对象的数量，大小等等，并支持对象查询语言。

生成heap.bin Dump文件后，使用jhat查看

```bash
jhat heap.bin
.....
Started HTTP server on port 7000
Server is ready.
```

访问 http://localhost:7000，就可以查看详细的内存信息

有时你Dump出来的堆很大，在启动时会报堆空间不足的错误，可以使用如下参数：

```bash
jhat -J-Xmx512m <heap dump file>
```

参考

[cnblogs.com](http://www.cnblogs.com/ggjucheng/archive/2013/04/16/3024986.html)
[csdn.net](http://blog.csdn.net/gtuu0123/article/details/6039474)
[iteye.com](http://gao-xianglong.iteye.com/blog/2173140)