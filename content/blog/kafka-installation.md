+++
date = "2017-03-21T23:14:11+08:00"
title = "安装Kafka"
categories = ["Engineering"]
tags = ["Kafka"]
description = "本文记录Apache Kafka的安装过程"
slug = "kafka-installation"
+++

### 安装

安装过程比较简单：

```bash
# 下载安装文件
wget -c http://mirrors.hust.edu.cn/apache/kafka/0.10.2.0/kafka_2.12-0.10.2.0.tgz
# 解压安装
mkdir -p /opt/kafka/
tar -zxvf kafka_2.12-0.10.2.0.tgz -C /opt/kafka/
```

### 运行模式

Kafka有三种运行模式，分别为：

* 单节点单Broker
* 单节点多Broker
* 多节点多Broker

#### 单节点单Broker

单节点单Broker需要以下步骤：

1. 启动Zookeeper
2. 启动Broker
3. 启动Consumer
4. 启动Producer

__启动Zookeeper__

ZK的配置位于`config/zookeeper.properties`，内容如下：

```console
dataDir=/tmp/zookeeper
clientPort=2181
maxClientCnxns=0
```

Zookeeper用于管理Kafka Broker和消费者。

```bash
cd /opt/kafka/kafka_2.12-0.10.2.0/
bin/zookeeper-server-start.sh config/zookeeper.properties
```

__启动Kafka Broker__

Broker配置位于`config/server.properties`，内容如下：

```console
broker.id=0

#listeners=PLAINTEXT://:9092

num.network.threads=3
num.io.threads=8
num.partitions=1
num.recovery.threads.per.data.dir=1

socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600

log.dirs=/tmp/kafka-logs
log.retention.hours=168
log.segment.bytes=1073741824
log.retention.check.interval.ms=300000

zookeeper.connect=localhost:2181
zookeeper.connection.timeout.ms=6000
```

启动Broker

```bash
bin/kafka-server-start.sh config/server.properties
```

__创建Topic__

创建名为`kafkatopic`的Topic（1 Partition, 1 Replica）

```bash
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic kafkatopic
```

查看创建的Topic

```bash
bin/kafka-topics.sh --list --zookeeper localhost:2181
# 查看详情
bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic kafkatopic
```

删除Topic

```bash
bin/kafka-topics.sh --delete --zookeeper localhost:2181 --topic kafkatopic
```

此时并没有完全删除znode，只是把相应的Topic的状态改成`marked for deletion`

如果需要彻底删除，需要修改`config/server.properties`的配置。

```console
# Switch to enable topic deletion or not, default value is false
#delete.topic.enable=true
```

但是如果一开始没有注意这个选项，那就不得不在Zookeeper里硬删除了。启动Zookeeper的Console，执行以下命令：

```bash
cd cd /opt/zookeeper/zookeeper-3.4.9/
bin/zkCli.sh

# 查看znode
ls /brokers/topics
[test, kafkatopic, __consumer_offsets]

# 删除znode
rmr /brokers/topics/kafkatopic
```

__启动Producer__

```bash
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic kafkatopic
```

* `--broker-list`，指定连接的Broker
* `--topic`，指定Topic

__启动Consumer__

默认的Consumer配置，位于`config/consumer.properties`：

```console
zookeeper.connect=127.0.0.1:2181
zookeeper.connection.timeout.ms=6000

group.id=test-consumer-group
```

启动Consumer

```bash
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic kafkatopic -from-beginning
```

#### 单节点多Broker

单节点多Broker需要以下步骤：

1. 启动Zookeeper
2. 启动Broker1/2/3
3. 启动Consumer
4. 启动Producer

__启动Zookeeper__

Zookeeper的启动同单节点单Broker，见上：

```bash
cd /opt/kafka/kafka_2.12-0.10.2.0/
bin/zookeeper-server-start.sh config/zookeeper.properties
```

__启动Kafka Broker1/2/3__

Broker1配置位于`config/server.properties`，内容如下：

```console
broker.id=0

#listeners=PLAINTEXT://:9092

num.network.threads=3
num.io.threads=8
num.partitions=1
num.recovery.threads.per.data.dir=1

socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600

log.dirs=/tmp/kafka-logs
log.retention.hours=168
log.segment.bytes=1073741824
log.retention.check.interval.ms=300000

zookeeper.connect=localhost:2181
zookeeper.connection.timeout.ms=6000
```

Broker2配置位于`config/server-1.properties`，内容如下：

```console
broker.id=1

listeners=PLAINTEXT://:9093

num.network.threads=3
num.io.threads=8
num.partitions=1
num.recovery.threads.per.data.dir=1

socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600

log.dirs=/tmp/kafka-logs-1
log.retention.hours=168
log.segment.bytes=1073741824
log.retention.check.interval.ms=300000

zookeeper.connect=localhost:2181
zookeeper.connection.timeout.ms=6000
```

Broker3配置位于`config/server-2.properties`，内容如下：

```console
broker.id=2

listeners=PLAINTEXT://:9094

num.network.threads=3
num.io.threads=8
num.partitions=1
num.recovery.threads.per.data.dir=1

socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600

log.dirs=/tmp/kafka-logs-2
log.retention.hours=168
log.segment.bytes=1073741824
log.retention.check.interval.ms=300000

zookeeper.connect=localhost:2181
zookeeper.connection.timeout.ms=6000
```

分别启动Broker1/2/3

```bash
bin/kafka-server-start.sh config/server.properties
bin/kafka-server-start.sh config/server-1.properties
bin/kafka-server-start.sh config/server-2.properties
```

__创建Topic__

创建名为`my-replicated-topic`的Topic（1 Partition, 3 Replica）

```bash
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 1 --topic my-replicated-topic
```

查看创建的Topic

```bash
# 查看详情
bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic my-replicated-topic

Topic:my-replicated-topic   PartitionCount:1    ReplicationFactor:3 Configs:
    Topic: my-replicated-topic  Partition: 0    Leader: 2   Replicas: 2,0,1 Isr: 2,0,1
```

__启动Producer__

```bash
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic my-replicated-topic
```

__启动Consumer__

```bash
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic my-replicated-topic --from-beginning
```

_异常处理_

关闭作为Master节点的`node-2`，这时，Broker会在1/2中重新选取，保证Broker功能的正常运行。

```console
bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic my-replicated-topic

Topic:my-replicated-topic   PartitionCount:1    ReplicationFactor:3 Configs:
    Topic: my-replicated-topic  Partition: 0    Leader: 0   Replicas: 2,0,1 Isr: 0,1
```

重启`node-2`后，Broker集群恢复正常。

```console
bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic my-replicated-topic

Topic:my-replicated-topic   PartitionCount:1    ReplicationFactor:3 Configs:
    Topic: my-replicated-topic  Partition: 0    Leader: 0   Replicas: 2,0,1 Isr: 0,1,2
```

#### 多节点多Broker

待补充

