+++
title = "线上CPU占用率过高的问题定位"
categories = ["Engineering"]
tags = ["Java"]
description = "CPU占用率过高的分析过程"
slug = "cat-cpu-issue-troubleshooting"
date = "2017-03-01T10:08:11+08:00"
+++

线上系统一个模块的CPU占用率过高，定位分析过程如下。

### 查看运行状态

登录到服务器查日志，没发现任何异常，并且系统的调用量也非常小，理论上不应该产生问题。

查看究竟CPU消耗在哪里了， 用`ps`命令按CPU的消耗排序，找出最耗CPU的具体线程。

```console
ps -mp 4754 -o THREAD,tid,time | sort -nk 2 -r

USER     %CPU PRI SCNT WCHAN  USER SYSTEM   TID     TIME
java      231   -    - -         -      -     - 117-20:42:05
java     15.0  19    - futex_    -      -  4789   7-16:31:35
java      8.2  19    - futex_    -      -  4782   4-05:08:12
java      8.2  19    - futex_    -      -  4781   4-05:09:24
java      8.2  19    - futex_    -      -  4780   4-05:05:17
```

### 分析

用`jstack`查看线程在干什么

```console
jstack 4754 | grep nid -A 30 | grep 12b5

...
"Concurrent Mark-Sweep GC Thread" os_prio=0 tid=0x00007ff0a815c000 nid=0x12b5 runnable
```

JVM在做GC

用`jstat`命令验证，果然，系统在不停的GC

```console
jstat -gc 29559 1 3

 S0C    S1C    S0U    S1U      EC       EU        OC         OU       MC     MU    CCSC   CCSU   YGC     YGCT    FGC    FGCT     GCT
52416.0 52416.0    0.0  0.0   419456.0 368622.4  1572864.0   1572864.0 50652.0 49501.0 5928.0 5699.8    1148   38.028   2104667   717190.628   717228.656
52416.0 52416.0    0.0  0.0   419456.0 368622.6  1572864.0   1572864.0 50652.0 49501.0 5928.0 5699.8    1148   38.028   2104668   717190.628   717228.656
52416.0 52416.0    0.0  0.0   419456.0 368622.6  1572864.0   1572864.0 50652.0 49501.0 5928.0 5699.8    1148   38.028   2104669   717192.053   717230.082
```

GC后内存并没有被回收掉，说明有内存泄漏？

### 查看监控

看看究竟是什么东西在内存里面，为了全面分析，直接dump出文件，然后用`jhat`查看里面的内容，发现`cat`占用的量很大

```console
313309 instance of class org.jboss.netty.channel.DefaultChannelPipeline$DefaultChannelHandlerContext
...
313293 instance of class com.dianping.cat.message.io.ChannelMessage$ExceptionHandler
...
10000 instance of class com.dianping.cat.message.internal.DefaultTransaction
10000 instance of class com.dianping.cat.message.spi.internal.DefaultMessageTree
...
```

查看cat的日志，发现一直在报错，连的server也不对。

```console
[02-21 11:49:23.949] [ERROR] [ChannelManager] Error when try to connecting to /10.0.1.81:2280
[02-21 11:49:24.081] [INFO] [ChannelManager] close channel null
```

原来cat客户端配置的服务器就不对。

为什么cat会引起系统内存爆掉呢？还是看看cat的原代码吧：

```java
public class TcpSocketSender implements Task, MessageSender, LogEnabled {
    public static final String ID = "tcp-socket-sender";
    public static final int SIZE = 10000;
    @Inject
    private MessageCodec m_codec;
    @Inject
    private MessageStatistics m_statistics;
    @Inject
    private ClientConfigManager m_configManager;
    private MessageQueue m_queue = new DefaultMessageQueue(10000);
    private List<InetSocketAddress> m_serverAddresses;
    ...
}
```

可以看出，队列里最多放10000个消息，这个和上面jhat的统计信息能对上，系统已经放了10000个DefaultTransaction对象，对消息内容不大的系统问题不大，但如果某个系统的cat消息内容大的话也需要特别留意。

有问题的这个系统，对应的cat的消息内容并不大，这点消息量也不会让系统内存爆掉的。

从`jhat`的统计信息里能看到，netty的连接数很大，channel对应的对象占了绝大多数，我们可以看看ChannelManager这个类，它是个task, 会定时去检查和client server的路由，如果连接没有建立的情况下会一直尝试建立连接，调用createChannel方法

```java
private ChannelFuture createChannel(InetSocketAddress address) {
    ChannelFuture future = null;

    try {
        future = m_bootstrap.connect(address);
        future.awaitUninterruptibly(100, TimeUnit.MILLISECONDS); // 100 ms

        if (!future.isSuccess()) {
            m_logger.error("Error when try to connecting to " + address);
            closeChannel(future);
        } else {
            m_logger.info("Connected to CAT server at " + address);
            return future;
        }
    } catch (Throwable e) {
        m_logger.error("Error when connect server " + address.getAddress(), e);

        if (future != null) {
            closeChannel(future);
        }
    }
    return null;
}
```

当连接建不起来的时候，会去关channel, 问题在于这个方法并没有把对象完全释放掉。 

所以，当正常情况下，不会去建立很多channel, 当cat连不上的时候， 一个定时的后台线程不停创建channel连接，发现有问题的时候关闭又释放不完全，导致内存爆掉。

对我们来说，保证cat配置正确和可用可以规避这个问题；当然，cat的代码也可以优化来解决这个问题。
