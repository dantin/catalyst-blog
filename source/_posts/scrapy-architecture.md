---
title: Scrapy架构
date: 2016-01-19 11:26:37
categories: 工程
tags: [Scrapy, Python]
toc: true
---

[Scrapy](http://scrapy.readthedocs.org/)是一个基于Python和Twisted的爬虫框架，在之前的项目里用了一些，这里对它的架构做一下记录。

### 架构

下图展示了Scrapy的架构，包括它的组件和数据流（绿色线条标识）。

![Scrapy架构](/images/scrapy-architecture.png "Scrapy-architecture")

#### 组件

* Scrapy Engine，Scrapy引擎

    引擎控制各组件间的数据流动，以及某一事件发生时触发注册的动作。

* Scheduler，调度器

    调度器把引擎的事件请求排队，在事件到达时将事件重新发送给引擎，并触发响应的动作。

* Downloader，下载器

    下载器负责抓取网页给引擎，然后由引擎分发给爬虫。

* Spiders，爬虫

    爬虫是Scrapy使用者写的自定义类，它负责解析网页（parse response）、抓取数据（extract item）、跟踪外链（follow link）等。一般一个爬虫与一个域名一一对应。

* Item Pipeline

    Item Pipeline负责处理爬取结果，例如：数据清理、验证和持久化。

* Downloader middlewares

    对接引擎和下载器，可以在发请求前和接受网页返回后插入一些自定义代码，如：设置HTTP头部的UserAgent等。

* Spider middlewares

    对接引擎和爬虫，可以在爬虫接收请求前和输出抓取数据后插入一些自定义代码

#### 数据流

Scrapy的数据流由它的引擎控制，工作方式如下：

1. 引擎打开一个网站，找到网站域名对应的爬虫。
2. 引擎通过爬虫获取起始URL，并把起始URL以Request对象的方式提交给调度器。
3. 引擎从调度器请求下一个待爬取的URL。
4. 调度器返回URL给引擎，引擎把这个URL通过Downloader Middleware分发给下载器（request direction）。
5. 下载完毕后，下载器生成Response对象，并通过Downloader Middleware返回给引擎（response direction）。
6. 引擎拿到Response对象后，通过Spider middlewares分发给爬虫（input direction）。
7. 爬虫处理好Response对象后，抓取需要的数据（scraped item），生成待跟踪外链（New Request）给引擎。
8. 引擎把抓取的数据给Item Pipeline，把New Request给调度器。
9. 数据流迭代（至Step 2），直到调度器中的Request全部爬取完为止，最后引擎关闭与网站的连接。

参考

__[Scrapy官方文档](http://scrapy.readthedocs.org/en/latest/topics/architecture.html)__