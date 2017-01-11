+++
date = "2016-02-17T10:20:16+08:00"
title = "Mastering ElasticSearch之一"
categories = ["Engineering"]
tags = ["Elastic Search"]
description = "本文记录《Mastering ElasticSearch》第一章的读书笔记"
slug = "elasticsearch-master-es-01"
+++

Introduction to ElasticSearch。

ElasticSearch的底层操作，如：创建索引、查询等，使用Apache Lucene。

### Introducing Apache Lucene

在了解ElasticSearch之前，不妨先看一下Apache Lucene。

#### Overall architecture

Lucence中常见的对象类型包括：

* Document: 文档，主要的数据承载体，也是Lucence索引的主要数据；
* Field: 文档的一部分，即："名/值"对，如：JSON中的域；
* Term: 可搜索的"词语"；
* Token: 包含Term，起始位置，类型等"原数据"；

Lucene的核心是反转索引，_inverted index_。

其基本结构是一个表，即：

```bash
+------+     +-------------+
| Term | --> | Document(s) |
+------+     +-------------+
```

举个反转索引的例子，假设有三篇文章：

1. ElasticSearch Server (document 1)
2. Mastering ElasticSearch (document 2)
3. Apache Solr 4 Cookbook (document 3)

创建反转索引后的结果如下：

| Term          | Count | Docs    |
| ------------- | ----- |:-------:|
| 4             | 1     | <3>     |
| Apache        | 1     | <3>     |
| Cookbook      | 1     | <3>     |
| ElasticSearch | 2     | <1>,<2> |
| Mastering     | 1     | <2>     |
| Server        | 1     | <1>     |
| Solr          | 1     | <3>     |

以上只是简单的示例，实际上反转索引包含的内容更多，如：_term vectors_。

索引存储的基本单位是_segment_，其特性是写一次，读多次。当_segments_增加时，为了提升系统的运行效率，还会有_segments merge_的过程。

#### Analyzing your data

查询和创建索引时都需要把文本变成Term，这就是所谓的"文本分析"。

分析工具是_analyzer_，通常包含_tokenizer_、一系列的_filter_和若干_character mappers_。

* tokenizer

    tokenizer把文本分成token，同时包含一些元信息，如：位置、原始文本、文本长度等。其结果是_token stream_。

* filter

    filter会改写、增加、转换_token stream_。filter串行执行，前一个filter产生的输出会作为后一个filter的输入。常见的如：

    * Lowercase filter
    * ASCII folding filter
    * Synonyms filter
    * Multiple language stemming filters

    Indexing和Querying的_analyzer_可以不同，在使用时需要注意。

### Lucene query language

Lucene中的query由term和operator组成。term可以是一个词或一个句子，如果query被设置成需要解析，那么在查询前会对每个term应用配置的解析器。

Lucene的Boolean operator分为：

* AND，与
* OR，或
* NOT，非
* \+，必须包含

    如：`+lucene apache`，匹配那些必须包含lucene、可能包含apache的文档。

* \-，必须不含

    如：`+lucene -elasticsearch`，匹配那些必须包含lucene、不含elasticsearch的文档。

Lucene支持复合操作符，如：

```bash
elasticsearch AND (mastering OR book)
```

#### Querying fields

Lucene中的数据逻辑上按Field保存，如果要在特定Field上查询，需要使用特定语法。

如：需要查找title中包含elasticsearch的文档，查询语句如下：

```bash
title:elasticsearch
```

它也支持组合查询：

```bash
title:(+elasticsearch +"mastering book")
```

其等价于：

```bash
+title:elasticsearch +title:"mastering book"
```

#### Term modifiers

* 通配符

    `*`，匹配任意；

    `?`，匹配单个字符。

* 模糊搜索

    `_~ + 数字_`

    `writer~2`可以匹配writer和writers。`title:"mastering elasticsearch"~2`可以匹配mastering elasticsearch和mastering book elasticsearch。

* Boost

    `^`

    `word^1.3`，为word增加权重。

* 范围搜索

    `[`和`]`

    ```console
    # 范围
    price:[10.00 TO 15.00]
    # 支持字符
    name:[Adam TO Adria]
    # 包含不包含
    price:[10.00 TO 15.00}
    ```

* 转义字符

    `\`

### Introducing ElasticSearch

下面是ElasticSearch相关的内容。

#### Basic concepts

* Index

    数据保存的地方，类似SQL中的数据库，保存Document(s)。

* Document

    JSON文档，每篇文章可能有多个Field；每个Field可能有一个或多个（multi-valued）值。

* Mapping

    存放自定义的索引配置，如：analyzer、filter、删除HTML标签、排序等。ElasticSearch本身有自动的Mapping机制，但默认的效果不一定好，一般需要自行配置。

* Type

    类似SQL中的表。一般而言，一种Document对应一种Type，一个Index可以包含多种Type。每个Type都有自己对应的Mapping。

* Node

    运行ElasticSearch Instance的节点。

* Cluster

    多个Node组成一个ElasticSearch的Cluster。

* Shard

    Lucene索引的分片，这样Cluster中的多个Node就能存放几乎无限大小的Index 。注意：这个配置只在Index创建的时候生效，后期不能改变。

* Replica

    Shard的拷贝，这样就能并行响应更多的请求。

* Gateway

    ElasticSearch存放自身信息的地方。

#### Key concepts behind ElasticSearch architecture

ElasticSearch的核心概念是易用性和可扩展性，出于此考虑，ElasticSearch的特性如下：

* 合理的默认值，安装后即可使用，支持自动配置和自动发现；
* 默认以分布式模式运行，新增节点可以自动加入集群；
* 无单点故障（_SPOF_，single point of failure），Shard的自动分布和拷贝；
* 容量和性能可扩展；
* 不限制索引中数据的组织形式；
* 搜索性能接近实时（_NRT_，Near Real Teim）；

#### Working of ElasticSearch

##### The boostrap process

ElasticSearch节点启动后，使用多播查找同一Cluster中的其他节点，并与之建立连接。

<img src="/images/elasticsearch-bootstrap-process.png" alt="ElasticSearch的启动过程" style="width: 500px;"/>
