---
title: Tcpdump备忘录
date: 2016-12-14 11:03:03
categories: 效率
tags: [Linux, Network]
toc: true
---

tcpdump是一个对网络数据包进行截获的包分析工具。

### tcpdump基础

tcpdump可以将网络中传送的数据包的“头”完全截获下来提供分析。它支持针对网络层、协议、主机、端口等的过滤，并支持与、或、非逻辑语句协助过滤有效信息。

命令使用规则如下：

```
Usage: tcpdump [-aAbdDefhHIJKlLnNOpqRStuUvxX] [ -B size ] [ -c count ]
        [ -C file_size ] [ -E algo:secret ] [ -F file ] [ -G seconds ]
        [ -i interface ] [ -j tstamptype ] [ -M secret ]
        [ -P in|out|inout ]
        [ -r file ] [ -s snaplen ] [ -T type ] [ -V file ] [ -w file ]
        [ -W filecount ] [ -y datalinktype ] [ -z command ]
        [ -Z user ] [ expression ]
```

过滤方式有很多，可以依据所需设置过滤条件，较常用的三种：

#### 按host过滤

```
tcpdump -i eth1 -n -X src host 10.19.66.62
```

#### 按port过滤

```
tcpdump -i eth1 -n -X src host 10.19.66.62 and dst port 80
```

#### 按protocol过滤

```
tcpdump -i eth1 -n -X src host 10.19.66.62 and dst port 80 and tcp
```

### 抓包过程

下面来看一下tcpdump过滤规则的具体使用：

我们在服务器144.168.60.135上搭建了一个http服务用来作为服务端，180.169.12.163作为客户端客户端对其发起访问。我们使用前面提到的按host 180.169.12.163、port 80以及protocol tcp的组合条件来执行tcpdump。

```
sudo tcpdump -i venet0 -n tcp port 80 and host 180.169.12.163

22:12:33.416541 IP 180.169.12.163.32864 > 144.168.60.135.http: Flags [S], seq 983822144, win 65535, options [mss 1386,nop,wscale 5,nop,nop,TS val 1312878687 ecr 0,sackOK,eol], length 0
22:12:33.416613 IP 144.168.60.135.http > 180.169.12.163.32864: Flags [S.], seq 3255622450, ack 983822145, win 14480, options [mss 1460,sackOK,TS val 163505529 ecr 1312878687,nop,wscale 7], length 0
22:12:33.783510 IP 180.169.12.163.32864 > 144.168.60.135.http: Flags [.], ack 1, win 4122, options [nop,nop,TS val 1312879052 ecr 163505529], length 0
22:12:33.785310 IP 180.169.12.163.32864 > 144.168.60.135.http: Flags [P.], seq 1:509, ack 1, win 4122, options [nop,nop,TS val 1312879055 ecr 163505529], length 508
22:12:33.785334 IP 144.168.60.135.http > 180.169.12.163.32864: Flags [.], ack 509, win 122, options [nop,nop,TS val 163505898 ecr 1312879055], length 0
22:12:33.790782 IP 144.168.60.135.http > 180.169.12.163.32864: Flags [P.], seq 1:182, ack 509, win 122, options [nop,nop,TS val 163505903 ecr 1312879055], length 181
22:12:34.419987 IP 180.169.12.163.32864 > 144.168.60.135.http: Flags [.], ack 182, win 4116, options [nop,nop,TS val 1312879688 ecr 163505903], length 0
22:12:34.580203 IP 180.169.12.163.32864 > 144.168.60.135.http: Flags [P.], seq 509:945, ack 182, win 4116, options [nop,nop,TS val 1312879846 ecr 163505903], length 436
22:12:34.580470 IP 144.168.60.135.http > 180.169.12.163.32864: Flags [P.], seq 182:362, ack 945, win 130, options [nop,nop,TS val 163506693 ecr 1312879846], length 180
22:12:34.888476 IP 180.169.12.163.32864 > 144.168.60.135.http: Flags [.], ack 362, win 4110, options [nop,nop,TS val 1312880143 ecr 163506693], length 0
22:12:36.605142 IP 180.169.12.163.32864 > 144.168.60.135.http: Flags [.], ack 362, win 4110, length 0
22:12:36.605327 IP 144.168.60.135.http > 180.169.12.163.32864: Flags [.], ack 945, win 130, options [nop,nop,TS val 163508718 ecr 1312880143], length 0
22:13:05.271611 IP 180.169.12.163.32864 > 144.168.60.135.http: Flags [F.], seq 945, ack 362, win 4110, options [nop,nop,TS val 1312910518 ecr 163508718], length 0
22:13:05.272333 IP 144.168.60.135.http > 180.169.12.163.32864: Flags [F.], seq 362, ack 946, win 130, options [nop,nop,TS val 163537385 ecr 1312910518], length 0
22:13:05.586112 IP 180.169.12.163.32864 > 144.168.60.135.http: Flags [.], ack 363, win 4110, options [nop,nop,TS val 1312910837 ecr 163537385], length 0
```

不同的协议类型有不同的数据包格式显示，以tcp包为例，通常tcpdump对tcp数据包的显示格式如下:

```
timestamp src > dst: flags data-seqno ack window urgent options
```

每一项的解释如下：

* `src ＞ dst`：表明从源地址到目的地址
* `flags`：TCP包中的标志信息，S 是SYN标志,，F (FIN)，P (PUSH)，R (RST)，”.” (没有标记)
* `data-seqno`：是数据包中的数据的顺序号
* `ack`：是下次期望的顺序号
* `window`：是接收缓存的窗口大小
* `urgent`：表明数据包中是否有紧急指针
* `options`：选项

执行抓包过程中输出的这八行数据其实包含了tcp三次握手和四次挥手的交互过程，详细分析下看看：

第一至三行为建立链接的三次握手过程，包状态为：[S]、[S.]、[.]

```
22:12:33.416541 IP 180.169.12.163.32864 > 144.168.60.135.http: Flags [S], seq 983822144, win 65535, options [mss 1386,nop,wscale 5,nop,nop,TS val 1312878687 ecr 0,sackOK,eol], length 0
22:12:33.416613 IP 144.168.60.135.http > 180.169.12.163.32864: Flags [S.], seq 3255622450, ack 983822145, win 14480, options [mss 1460,sackOK,TS val 163505529 ecr 1312878687,nop,wscale 7], length 0
22:12:33.783510 IP 180.169.12.163.32864 > 144.168.60.135.http: Flags [.], ack 1, win 4122, options [nop,nop,TS val 1312879052 ecr 163505529], length 0
```

第一行：客户端163向服务器135发送了一个序号seq 983822144给服务端；

第二行：服务端收到后将序号加一返回ack 983822145；

第三行：客户端检查返回值正确，向服务端发ack 1，建立了链接；

第四至十二行为传输数据的过程，包状态为[P.]、[.]；

```
22:12:33.785310 IP 180.169.12.163.32864 > 144.168.60.135.http: Flags [P.], seq 1:509, ack 1, win 4122, options [nop,nop,TS val 1312879055 ecr 163505529], length 508
22:12:33.785334 IP 144.168.60.135.http > 180.169.12.163.32864: Flags [.], ack 509, win 122, options [nop,nop,TS val 163505898 ecr 1312879055], length 0
22:12:33.790782 IP 144.168.60.135.http > 180.169.12.163.32864: Flags [P.], seq 1:182, ack 509, win 122, options [nop,nop,TS val 163505903 ecr 1312879055], length 181
22:12:34.419987 IP 180.169.12.163.32864 > 144.168.60.135.http: Flags [.], ack 182, win 4116, options [nop,nop,TS val 1312879688 ecr 163505903], length 0
22:12:34.580203 IP 180.169.12.163.32864 > 144.168.60.135.http: Flags [P.], seq 509:945, ack 182, win 4116, options [nop,nop,TS val 1312879846 ecr 163505903], length 436
22:12:34.580470 IP 144.168.60.135.http > 180.169.12.163.32864: Flags [P.], seq 182:362, ack 945, win 130, options [nop,nop,TS val 163506693 ecr 1312879846], length 180
22:12:34.888476 IP 180.169.12.163.32864 > 144.168.60.135.http: Flags [.], ack 362, win 4110, options [nop,nop,TS val 1312880143 ecr 163506693], length 0
22:12:36.605142 IP 180.169.12.163.32864 > 144.168.60.135.http: Flags [.], ack 362, win 4110, length 0
22:12:36.605327 IP 144.168.60.135.http > 180.169.12.163.32864: Flags [.], ack 945, win 130, options [nop,nop,TS val 163508718 ecr 1312880143], length 0
```

第四至十二行：具体的数据交互，tcpdump命令-x可以显示出具体内容；

第十三至十五行为关闭链接的四次挥手过程（ack延迟发送未禁用，所以这里只看到三个包），包状态为[F.]、[F.]、[.]。

```
22:13:05.271611 IP 180.169.12.163.32864 > 144.168.60.135.http: Flags [F.], seq 945, ack 362, win 4110, options [nop,nop,TS val 1312910518 ecr 163508718], length 0
22:13:05.272333 IP 144.168.60.135.http > 180.169.12.163.32864: Flags [F.], seq 362, ack 946, win 130, options [nop,nop,TS val 163537385 ecr 1312910518], length 0
22:13:05.586112 IP 180.169.12.163.32864 > 144.168.60.135.http: Flags [.], ack 363, win 4110, options [nop,nop,TS val 1312910837 ecr 163537385], length 0
```

第十三行：客户端发一个序号seq 945，说明要断开链接；

第十四行：服务端在收到后序号加一返回ack 946，同意断开链接；

第十五行：客户端检查返回值正确，向服务端发ack，链接断开。

### 高级用法

以上的分析是使用基本的过滤条件组合获取的，如果想要获取到限制条件更严格的报文数据应该怎么写命令呢？比如在数据交互时状态为[P.]. 即PSH-ACK，如果我们要抓取flag为[P.]的包应该怎么实现呢？

这里先挂一下tcp包头的桢格式（详解可参考TCP/IP协议），以便进一步说明如何使用tcpdump的过滤功能，头部固定为20字节，每行4字节，根据协议规则可以看到各个字节中存放的内容的含义。

```
 0               1               2               3
 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |        Destination Port       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        Sequence Number                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                   Acknowledgement Number                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Data |           |U|A|P|R|S|F|                               |
| Offset|  Reserved |R|C|S|S|Y|I|             Window            |
|       |           |G|K|H|T|N|N|                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|             Checksum          |         Urgnent Pointer       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                   Options                     |    Padding    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                              Data                             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

图中控制标志位在第13字节（从0开始计数）。从右往左这些位被依次编号为0到7, 而PSH位在3号，ACK在第4位，因此我们想抓取状态为[P.]的包表达式应写为tcp13=16+8=24。

执行命令

```
tcpdump -i eth1 -n -X src host 10.19.66.62 and dst port 80 and tcp[13]=24
```

此时加上-X参数可以以16进制和ASCII码形式打印出包数据，便于观察。

如果要抓取业务中的get请求包，怎么实现呢？首先查ASCII码表得”GET+空”的十六进制是0x47455420，因此表达式应为tcp[20:4]=0x47455420。

执行命令

```
tcpdump -i eth1 -n -A src host 10.19.66.62 and dst port 80 and tcp[20:4]=0x47455420
```

此时加上-A参数以ASCII码方式显示数据包，可以看到很方便的抓到了特定状态的包。

抓取到的输出如下如，可以看到get请求的具体信息了。以此推论，我们还可以把tcpdump用来统计get、post请求的访问次数等。

参考：

[高效运维的公众号](http://mp.weixin.qq.com/s?__biz=MzA4Nzg5Nzc5OA==&mid=2651660526&idx=1&sn=fca5b6ee36cf8f4b2baeb2434439e48e&mpshare=1&scene=1&srcid=0629ZXbSTNNY2w1SNiMb8brG#rd)