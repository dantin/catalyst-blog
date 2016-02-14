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
