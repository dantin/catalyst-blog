+++
date = "2017-07-25T15:46:57+08:00"
title = "Sysbench备忘录"
slug = "tools-sysbench-memo"
categories = ["Misc"]
tags = ["Tools", "Memo"]
description = "本文介绍Sysbench的使用"
+++

Sysbench是一个模块化的、跨平台、多线程基准测试工具，主要用于评估测试各种不同系统参数下的数据库负载情况。它主要包括以下几种方式的测试：

1. CPU性能
2. 磁盘IO性能
3. 调度程序性能
4. 内存分配及传输速度
5. POSIX线程性能
6. 数据库性能(OLTP基准测试)

目前Sysbench支持包括MySQL, Oracle在内的数据库。

### 安装

根据不同的操作系统环境，选择不同的安装包

CentOS

```console
curl -s https://packagecloud.io/install/repositories/akopytov/sysbench/script.rpm.sh | sudo bash
sudo yum -y install sysbench
```

MaxOS

```console
# Add --with-postgresql if you need PostgreSQL support
brew install sysbench
```

源码安装

```console
yum -y install make automake libtool pkgconfig libaio-devel vim-common
# For MySQL support, replace with mysql-devel on RHEL/CentOS 5
yum -y install mariadb-devel
# For PostgreSQL support
#yum -y install postgresql-devel

./autogen.sh
# Add --with-pgsql to build with PostgreSQL support
./configure
make
make install
```

### CPU

CPU测试主要是进行素数的加法运算，在下面的例子中，指定了最大的素数为20000，自己可以根据机器CPU的性能来适当调整数值。

```console
sysbench cpu --cpu-max-prime=20000 run
```

### 线程测试

```console
sysbench threads --threads=64 --thread-yields=100 --thread-locks=2 run
```

### 磁盘IO性能测试

最大创建16个线程，创建的文件总大小为3G，文件读写模式为随机读。

```console
sysbench fileio --threads=16 --file-total-size=3G --file-test-mode=rndrw prepare
sysbench fileio --threads=16 --file-total-size=3G --file-test-mode=rndrw run
sysbench fileio --threads=16 --file-total-size=3G --file-test-mode=rndrw cleanup
```

### Mutex测试

```console
sysbench mutex --threads=16 --mutex-num=1024 --mutex-locks=10000 --mutex-loops=5000 run
```

### 内存

在内存中传输 4G 的数据量，每个 block 大小为 8K。

```console
sysbench memory --memory-block-size=8k --memory-total-size=4G run
```

### 数据库

一项测试开始前需要用prepare来准备好表和数据，run执行真正的压测，cleanup用来清除数据和表。

```console
sysbench ./lua-tests/db/oltp.lua --db-driver=mysql \
--mysql-host=10.3.3.129 --mysql-port=3306 --mysql-user=root --mysql-password= \
--mysql-db=sbtest --oltp-tables-count=16 --oltp-table-size=5000 --oltp-dist-type=special --oltp-dist-pct=1 --oltp-dist-res=50 --threads=256 --events=2000000000 --oltp-read-only=off --report-interval=1 --rand-type=uniform --time=200 --percentile=99 [prepare|run|cleanup]
```

__参数说明__

* `--mysql-db=dbtest`：测试使用的目标数据库，这个库名要事先创建
* `--oltp-tables-count=10`：产生表的数量
* `--oltp-table-size=5000`：每个表产生的记录行数
* `--oltp-dist-type=uniform`：指定随机取样类型，可选值有 uniform(均匀分布), Gaussian(高斯分布), special(空间分布)。默认是special
* `--oltp-read-only=off`：表示不止产生只读SQL，也就是使用oltp.lua时会采用读写混合模式。默认 off，如果设置为on，则不会产生update,delete,insert的sql。
* `--oltp-test-mode=nontrx`：执行模式，这里是非事务式的。可选值有simple,complex,nontrx。默认是complex
  * simple：简单查询，SELECT c FROM sbtest WHERE id=N
  * complex (advanced transactional)：事务模式在开始和结束事务之前加上begin和commit， 一个事务里可以有多个语句，如点查询、范围查询、排序查询、更新、删除、插入等，并且为了不破坏测试表的数据，该模式下一条记录删除后会在同一个事务里添加一条相同的记录。
  * nontrx (non-transactional)：与simple相似，但是可以进行update/insert等操作，所以如果做连续的对比压测，你可能需要重新cleanup,prepare。
* `--oltp-skip-trx=on|off`：省略begin/commit语句。默认是off
* `--rand-init=on`：是否随机初始化数据，如果不随机化那么初始好的数据每行内容除了主键不同外其他完全相同
* `--threads=12`： 并发线程数，可以理解为模拟的客户端并发连接数
* `--report-interval=10`：表示每10s输出一次测试进度报告
* `--events=0`：压力测试产生请求的总数，如果以下面的time来记，这个值设为0
* `--max-time=120`：压力测试的持续时间，这里是2分钟。

注意，针对不同的选项取值就会有不同的子选项。比如`oltp-dist-type=special`，就有比如`oltp-dist-pct=1`、`oltp-dist-res=50`两个子选项，代表有50%的查询落在1%的行（即热点数据）上，另外50%均匀的(sample uniformly)落在另外99%的记录行上。

再比如`oltp-test-mode=nontrx`时, 就可以有`oltp-nontrx-mode`，可选值有select（默认）, update_key, update_nokey, insert, delete，代表非事务式模式下使用的测试sql类型。

以上代表的是一个只读的例子，可以把`threads`依次递增（16,36,72,128,256,512），或者调整my.cnf参数，比较效果。

另外需要注意的是，大部分mysql中间件对事务的处理，默认都是把sql发到主库执行，所以只读测试需要加上oltp-skip-trx=on来跳过测试中的显式事务。

### 结果解读

```console
sysbench 1.0.8 (using bundled LuaJIT 2.1.0-beta2)

Running the test with following options:
Number of threads: 256
Report intermediate results every 1 second(s)
Initializing random number generator from current time
Initializing worker threads...

Threads started!

[ 1s ] thds: 256 tps: 812.14 qps: 20231.65 (r/w/o: 14698.16/3656.11/1877.38) lat (ms,99%): 759.88 err/s: 0.00 reconn/s: 0.00
...


SQL statistics:
    queries performed:
        read:                            5178110   //总select数量
        write:                           1479460   //总update、insert、delete语句数量
        other:                           739730    //commit、unlock tables以及其他mutex的数量
        total:                           7397300
    transactions:                        369865 (1847.17 per sec.)   //通常需要关注的数字(TPS)
    queries:                             7397300 (36943.37 per sec.)
    ignored errors:                      0      (0.00 per sec.)      // 忽略的错误数
    reconnects:                          0      (0.00 per sec.)

General statistics:
    total time:                          200.2318s  // 即time指定的压测实际
    total number of events:              369865     // 总的事件数，一般与transactions相同

Latency (ms):
         min:                                 11.03
         avg:                                138.46  // 95%的语句的平均响应时间
         max:                                767.18
         99th percentile:                    320.17
         sum:                            51211838.92

Threads fairness:
    events (avg/stddev):           1444.7852/17.67
    execution time (avg/stddev):   200.0462/0.07

```

我们一般关注的用于绘图的指标主要有：

* response time avg: 平均响应时间。（后面的95%的大小可以通过--percentile=98的方式去更改）
* transactions: 精确的说是这一项后面的TPS 。但如果使用了-oltp-skip-trx=on，这项事务数恒为0，需要用total number of events 去除以总时间，得到tps（其实还可以分为读tps和写tps）
* read/write requests: 用它除以总时间，得到吞吐量QPS

参考：

* [Sysbench Manual](http://imysql.com/wp-content/uploads/2014/10/sysbench-manual.pdf)
* [Sysbench对MySQL压力测试](http://seanlook.com/2016/03/28/mysql-sysbench/)