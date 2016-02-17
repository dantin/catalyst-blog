title: master elasticsearch
tags:
---


### Introduction to ElasticSearch

#### Introducing Apache Lucene

ES的底层（建索引、查询）使用Apache Lucene。

##### Overall architecture

Lucence的类型如下：

* Document: 文档，主要的数据承载体，也是Lucence索引的数据
* Field: 文档的一部分，包含"名/值"对
* Term: 可搜索的"词语"
* Token: 包含Term，起始位置，类型等"原数据"

Lucene的核心是反转索引，即：_inverted index_。

其基本结构是：

```bash
+------+     +-------------+
| Term | --> | Document(s) |
+------+     +-------------+
```

比如，下面三篇文章：

1. ElasticSearch Server (document 1)
2. Mastering ElasticSearch (document 2)
3. Apache Solr 4 Cookbook (document 3)

创建的反转索引结果。

| Term          | Count | Docs    |
| ------------- | ----- |:-------:|
| 4             | 1     | <3>     |
| Apache        | 1     | <3>     |
| Cookbook      | 1     | <3>     |
| ElasticSearch | 2     | <1> <2> |
| Mastering     | 1     | <2>     |
| Server        | 1     | <1>     |
| Solr          | 1     | <3>     |

以上只是简单的例子，实际上的反转索引包含的内容可能还包括：_term vectors_等。

索引的存储单位是_segment_，（写一次，读多次），这就会有_segments merge_过程。

##### Analyzing your data

查询和创建索引时都需要把文本变成Term，这就是所谓的"文本分析"。

分析工具是_analyzer_，通常包含_tokenizer_、一系列的_filter_和若干_character mappers_。

* tokenizer

    tokenizer把文本分成token，同时包含一些元信息，如：位置、原始文本、文本长度等。其结果是_token stream_。

* filter

    filter会改写、增加、转换_token stream_，常见的如：

    * Lowercase filter
    * ASCII folding filter
    * Synonyms filter
    * Multiple language stemming filters

    filter串行执行，前一个产生的输出会作为后一个的输入。

Indexing和Querying的_analyzer_可以不同，因此在使用时需要当心。

#### Lucene query language

Lucene中的query由term和operator组成。term可以是一个词或一个句子，如果query被设置成需要解析，那么在查询前会对每个term应用配置的解析器。

Lucene的Boolean operator分为：

* AND
* OR
* NOT
* \+，必须包含

    如：`+lucene apache`，documents that match lucene term and may match apache term

* \-，必须不含

    如：`+lucene -elasticsearch`，document with lucene term, but not elasticsearch term

复合操作符

```bash
elasticsearch AND (mastering OR book)
```

##### Querying fields

Lucene的数据逻辑上按Field保存，如要在特定Field上查询某些内容，需使用特定语法。

如：需要查询title中包含elasticsearch的文档，查询语句如下：

```bash
title:elasticsearch
```

也支持组合查询：

```bash
title:(+elasticsearch +"mastering book")
```

等价于

```bash
+title:elasticsearch +title:"mastering book"
```

##### Term modifiers

通配符：'\*'，匹配任意；'?'，匹配单个字符。

模糊搜索：_~ + 数字_的形式出现。

Boost：'^'

范围搜索：'['和']'，如：`price:[10.00 TO 15.00]`；当然，也支持字符，如`name:[Adam TO Adria]`；以及包不包含：`price:[10.00 TO 15.00}`

转义字符：'\\'

#### Introducing ElasticSearch

##### Basic concepts

* Index

    数据保存的地方，类似SQL中的数据库，保存documents

* Document

    JSON格式，每篇文章可能有多个Field；每个Field可能有一个或多个（multi-valued）值。

* Mapping

    存放自定义的索引配置，如：analyzer、filter、删除HTML标签、排序等。ES本身有自动的Mapping机制，但默认的效果不一定好，一般需要自己配置。

* Type

    类似SQL中的表。一种Document对应一种Type，一个Index可以包含多种Type。每个Type有自己对应的Mapping。

* Node

    运行ElasticSearch Instance的节点。

* Cluster

    多个Node组成一个ElasticSearch的Cluster。

* Shard

    Lucene索引的分片，这样Cluster中的多个Node就能存放几乎无限大小的Index 。注意：这个配置只在Index创建的时候生效，后期不能改变。

* Replica

    Shard的拷贝，这样就能并行响应更多的请求。

* Gateway

    ElasticSearch自身信息存放的地方。

##### Key concepts behind ElasticSearch architecture


