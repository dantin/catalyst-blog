+++
date = "2016-08-22T12:13:02+08:00"
title = "ElasticSearch聚合分析API"
categories = ["Engineering"]
tags = ["Elastic Search"]
description = "本文记录Elastic Search的聚合API"
slug = "elasticsearch-api-aggs"
+++

聚合功能为ES注入了统计分析的血统，使用户在面对大数据提取统计指标时变得游刃有余。同样的工作，你在Hadoop中可能需要写MapReduce或Hive，在Mongo中你必须得用大段的MapReduce脚本，而在ES中仅仅调用一个API就能实现了。

### 概念

Aggregations的部分特性类似于SQL语言中的GROUP BY，AVG，SUM等函数。但Aggregations API还提供了更加复杂的统计分析接口。

掌握Aggregations需要理解两个概念：

* 桶(Buckets)：符合条件的文档的集合，相当于SQL中的GROUP BY。比如，在users表中，按“地区”聚合，一个人将被分到北京桶或上海桶或其他桶里；按“性别”聚合，一个人将被分到男桶或女桶；
* 指标(Metrics)：基于Buckets的基础上进行统计分析，相当于SQL中的COUNT, AVG, SUM等。比如，按“地区”聚合，计算每个地区的人数，平均年龄等；

对照一条SQL来加深我们的理解：

```sql
SELECT COUNT(color) FROM table GROUP BY color
```

GROUP BY相当于做分桶的工作，COUNT是统计指标。

下面介绍一些常用的Aggregations API。

### Metrics

#### AVG

求均值。

```bash
GET /company/employee/_search
{
    "aggs" : {
        "avg_grade" : { "avg" : { "field" : "grade" } }
    }
}
```

执行结果

```bash
{
    "aggregations": {
        "avg_grade": {"value": 75}
    }
}
```

其他的简单统计API，如valuecount, max，min，sum作用与SQL中类似，就不一一解释了。

#### Cardinality

Cardinality的作用是先执行类似SQL中的DISTINCT操作，然后再统计排重后集合长度。得到的结果是一个近似值，因为考虑到在大量分片中排重的性能损耗Cardinality算法并不会load所有的数据。

```bash
{
    "aggs" : {
        "author_count" : {
            "cardinality" : {"field" : "author"}
        }
    }
}
```

#### Stats

返回聚合分析后所有有关stat的指标。具体哪些是stat指标是ES定义的，共有5项。

```bash
{
    "aggs" : {
        "grades_stats" : { "stats" : { "field" : "grade" } }
    }
}
```

执行结果

```bash
{
    "aggregations": {
        "grades_stats": {
            "count": 6,
            "min": 60,
            "max": 98,
            "avg": 78.5,
            "sum": 471
        }
    }
}
```

#### Extended Stats

返回聚合分析后所有指标，比Stats多三个统计结果：平方和、方差、标准差

```bash
{
    "aggs" : {
        "grades_stats" : { "extended_stats" : { "field" : "grade" } }
    }
}
```

执行结果

```bash
{
    "aggregations": {
    "grade_stats": {
        "count": 9,
        "min": 72,
        "max": 99,
        "avg": 86,
        "sum": 774,
        # 平方和
        "sum_of_squares": 67028,
        # 方差
        "variance": 51.55555555555556,
        # 标准差
        "std_deviation": 7.180219742846005,
        #平均加/减两个标准差的区间，用于可视化你的数据方差
        "std_deviation_bounds": {
        "upper": 100.36043948569201,
        "lower": 71.63956051430799
        }
    }
    }
}
```

#### Percentiles

百分位法统计，举例，运维人员记录了每次启动系统所需要的时间，或者，网站记录了每次用户访问的页面加载时间，然后对这些时间数据进行百分位法统计。我们在测试报告中经常会看到类似的统计数据

```bash
{
    "aggs" : {
        "load_time_outlier" : {
            "percentiles" : {"field" : "load_time"}
        }
    }
}
```

结果是

```bash
{
    "aggregations": {
        "load_time_outlier": {
            "values" : {
            "1.0": 15,
            "5.0": 20,
            "25.0": 23,
            "50.0": 25,
            "75.0": 29,
            "95.0": 60,
            "99.0": 150
            }
        }
    }
}
```

加载时间在15ms内的占1%，20ms内的占5%，等等。

我们还可以指定百分位的指标，比如只想统计95%、99%、99.9%的加载时间

```bash
{
    "aggs" : {
        "load_time_outlier" : {
            "percentiles" : {
            "field" : "load_time",
            "percents" : [95, 99, 99.9]
            }
        }
    }
}
```

#### Percentile Ranks

Percentile API中，返回结果values中的key是固定的0-100间的值，而Percentile Ranks返回值中的value才是固定的，同样也是0到100。例如，我想知道加载时间是15ms与30ms的数据，在所有记录中处于什么水平，以这种方式反映数据在集合中的排名情况。

```bash
{
    "aggs" : {
        "load_time_outlier" : {
            "percentile_ranks" : {
            "field" : "load_time",
            "values" : [15, 30]
            }
        }
    }
}
```

执行结果

```bash
{
    "aggregations": {
        "load_time_outlier": {
            "values" : {
            "15": 92,
            "30": 100
            }
        }
    }
}
```

### Bucket

#### Filter

先过滤后聚合，类似SQL中的WHERE，也有点象GROUP BY后加HAVING。比如

```bash
{
    "aggs" : {
        "red_products" : {
            "filter" : { "term": { "color": "red" } },
            "aggs" : {
                "avg_price" : { "avg" : { "field" : "price" } }
            }
        }
    }
}
```

只统计红色衣服的均价。

#### Range

反映数据的分布情况，比如我想知道小于50，50到100，大于100的数据的个数。

```bash
{
    "aggs" : {
        "price_ranges" : {
            "range" : {
            "field" : "price",
            "ranges" : [
                { "to" : 50 },
                { "from" : 50, "to" : 100 },
                { "from" : 100 }
            ]
            }
        }
    }
}
```

执行结果

```bash
{
    "aggregations": {
    "price_ranges" : {
        "buckets": [
        {"to": 50, "doc_count": 2},
        {"from": 50, "to": 100, "doc_count": 4},
        {"from": 100, "doc_count": 4}
        ]
    }
    }
}
```

#### Missing

我们想找出price字段值为空的文档的个数。

```bash
{
    "aggs" : {
        "products_without_a_price" : {
            "missing" : { "field" : "price" }
        }
    }
}
```

执行结果

```bash
{
    "aggs" : {
        "products_without_a_price" : {
            "doc_count" : 10
        }
    }
}
```

#### Terms

针对某个字段去重后统计个数。

```bash
{
    "aggs" : {
        "genders" : {
            "terms" : { "field" : "gender" }
        }
    }
}
```

执行结果

```bash
{
    "aggregations" : {
        "genders" : {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 0,
            "buckets" : [
            {"key" : "male","doc_count" : 10},
            {"key" : "female","doc_count" : 10},
            ]
        }
    }
}
```

#### Date Range

针对日期型数据做分布统计。

```bash
{
    "aggs": {
        "range": {
            "date_range": {
            "field": "date",
            "format": "MM-yyy",
                "ranges": [
                { "to": "now-10M/M" },
                { "from": "now-10M/M" }
            ]
            }
        }
    }
}
```

这里的format参数是指定返回值的日期格式。

执行结果

```bash
{
    "aggregations": {
        "range": {
            "buckets": [
            {"to": 1.3437792E+12, "to_as_string": "08-2012","doc_count": 7},
            {"from": 1.3437792E+12, "from_as_string": "08-2012","doc_count": 2}
            ]
        }
    }
}
```

#### Global Aggregation

指定聚合的作用域与查询的作用域没有关联。因此返回结果中query命中的文档，与聚合的的统计结果是没有关系的。

```bash
{
    "query" : {
    "match" : { "title" : "shirt" }
    },
    "aggs" : {
        "all_products" : {
            "global" : {},
            "aggs" : {
                "avg_price" : { "avg" : { "field" : "price" } }
            }
        }
    }
}
```

这里的global指定聚合作用域。

#### Histogram

跟range类似，不过Histogram不需要你指定统计区间，只需要提供一个间隔区间的值。好象不太好理解，看个例子就全明白了。

比如，以50元为一个区间，统计每个区间内的价格分布

```bash
{
    "aggs" : {
        "prices" : {
            "histogram" : {
                "field" : "price",
                "interval" : 50
            }
        }
    }
}
```

执行结果

```bash
{
    "aggregations": {
        "prices" : {
            "buckets": [
            {"key": 0, "doc_count": 2},
            {"key": 50, "doc_count": 4},
            {"key": 100, "doc_count": 0},
            {"key": 150, "doc_count": 3}
            ]
        }
    }
}
```

由于最高的价格没超过200元，因此最后的结果自动分为小于50，50到100，100到150，大于150共四个区间的值。

100到150区间的文档数为0个，我们想在返回结果中自动过滤该值，或者过滤偏小的值，可以添加一个参数”min_doc_count”，比如

```bash
{
    "aggs" : {
    "prices" : {
        "histogram" : {
            "field" : "price",
            "interval" : 50,
            "min_doc_count" : 1
        }
    }
    }
}
```

返回结果会自动将你设定的值以下的统计结果过滤出去。

#### Date Histogram

使用方法与Histogram类似，只是聚合的间隔区间是针对时间类型的字段。

```bash
{
    "aggs" : {
    "articles_over_time" : {
        "date_histogram" : {
            "field" : "date",
            "interval" : "1M",
            "format" : "yyyy-MM-dd"
        }
    }
    }
}
```

执行结果

```bash
{
    "aggregations": {
    "articles_over_time": {
        "buckets": [
        {"key_as_string": "2013-02-02","key": 1328140800000, "doc_count": 1},
        {"key_as_string": "2013-03-02","key": 1330646400000, "doc_count": 2},
        ...
        ]
    }
    }
}
```

#### IPv4 range

由于ES是一个企业级的搜索和分析的解决方案，在做大量数据统计分析时比如用户访问行为数据，会采集用户的IP地址，类似这样的数据(还有地理位置数据等)，ES也提供了最直接的统计接口。

```bash
{
    "aggs" : {
    "ip_ranges" : {
        "ip_range" : {
        "field" : "ip",
        "ranges" : [
            { "to" : "10.0.0.5" },
            { "from" : "10.0.0.5" }
        ]
        }
    }
    }
}
```

执行结果

```bash
{
    "aggregations": {
    "ip_ranges": {
        "buckets" : [
        {"to": 167772165, "to_as_string": "10.0.0.5","doc_count": 4},
        {"from": 167772165,"from_as_string": "10.0.0.5","doc_count": 6}
        ]
    }
    }
}
```

#### Return only aggregation results

在统计分析时我们有时候并不需要知道命中了哪些文档，只需要将统计的结果返回给我们。因此我们可以在request body中添加配置参数size。

```bash
curl -XGET 'http://localhost:9200/twitter/tweet/_search' -d '{
    "size": 0,
    "aggregations": {
        "my_agg": {
            "terms": {"field": "text"}
            }
    }
}
'
```

### 聚合缓存

ES中经常使用到的聚合结果集可以被缓存起来，以便更快速的系统响应。这些缓存的结果集和你掠过缓存直接查询的结果是一样的。因为，第一次聚合的条件与结果缓存起来后，ES会判断你后续使用的聚合条件，如果聚合条件不变，并且检索的数据块未增更新，ES会自动返回缓存的结果。

注意聚合结果的缓存只针对size=0的请求(参考3.10章节)，还有在聚合请求中使用了动态参数的比如Date Range中的now(参考3.5章节)，ES同样不会缓存结果，因为聚合条件是动态的，即使缓存了结果也没用了。

参考

[大涌日志](http://www.tianyiqingci.com/2016/04/11/esaggsapi/)