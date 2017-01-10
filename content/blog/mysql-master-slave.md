+++
date = "2016-04-15T14:45:53+08:00"
title = "应用层的数据库读写分离方案"
categories = ["Engineering"]
tags = ["MySQL", "Spring", "Mybatis"]
description = "MySQL主从配置及读写分离总结"
slug = "mysql-master-slave"
+++

初创公司刚开始的时候，一般都是单机数据库；然而当流量上来了，就不得不考虑数据库集群了。一般的话，读都会比写多，差不多8:2的比例，具体业务具体不同。

本文是对之前的数据库读写分离文章的一个总结。

### 配置MySQL数据库的主从

* [MySQL主从复制介绍及搭建](/blog/mysql-master-slave-replication/)
 
### 常见的解决数据库读写分离方案

#### 应用层

* [程序实现MySQL数据库读写分离](/blog/spring-mybatis-mysql-seperate-master-and-slave/)
* [Spring MyBatis多数据源的配置和管理](/blog/spring-mybatis-mysql-multiply-data-source/)
* [Dynamic DataSource Routing](https://spring.io/blog/2007/01/23/dynamic-datasource-routing)
* [spring实现数据库读写分离](http://neoremind.net/2011/06/spring实现数据库读写分离)
 
#### 中间件

* [MySQL中间件研究](http://www.guokr.com/blog/475765/)
* [mysql-proxy](http://hi.baidu.com/geshuai2008/item/0ded5389c685645f850fab07)
* [Amoeba for MySQL](https://segmentfault.com/a/1190000003767988)

参考

[在应用层通过spring特性解决数据库读写分离](http://jinnianshilongnian.iteye.com/blog/1720618)