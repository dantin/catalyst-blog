---
title: Spring Data JPA -- Introduction
date: 2016-12-19 10:03:12
categories: 工程
tags: [Spring]
toc: true
---

使用Java Persistence API创建持久化层需要一部分模版代码，如：

1. 一个所有持久化对象共同使用的CRUD抽象类；
2. 继承此抽象类的具体类；

如果只针对一个项目，那么这些看起来不错，但是如果每个项目都需要这么实现一遍，事情就不那么靠谱了。

[Spring Data JPA](http://projects.spring.io/spring-data-jpa/)要解决的问题就是通用的数据持久层。

> Implementing a data access layer of an application has been cumbersome for quite a while. Too much boilerplate code has to be written to execute simple queries as well as perform pagination, and auditing. Spring Data JPA aims to significantly improve the implementation of data access layers by reducing the effort to the amount that’s actually needed. As a developer you write your repository interfaces, including custom finder methods, and Spring will provide the implementation automatically

### 什么是Spring Data JPA

__Spring Data JPA不是JPA Provider__。它是在JPA Provider之上的一层抽象，包含三部分：

* [Spring Data JPA](http://projects.spring.io/spring-data-jpa/)：实现Database相关功能，实现Spring Data Commons中定义的JPA持久化抽象接口；
* [Spring Data Commons](https://github.com/spring-projects/spring-data-commons)：所有[Spring Data Project](http://projects.spring.io/spring-data/)共用的基础抽象层；
* JPA Provider：提供Java Persistence API；

三层之间的关系如下：

```
  +-----------------+
  | Spring Data JPA |
  +--------+--------+
          /|\
           |
+---------------------+
| Spring Data Commons |
+----------+----------+
          /|\
           |
   +--------------+
   | JPA Provider |
   +--------------+
```

初看起来Spring Data JPA似乎增加了应用复杂度，但实际上它把我们从模版代码中解放出来。

### Repository接口

Spring Data JPA的关键在于它实现的Spring Data Commons数据抽象层，我们可以不了解具体的抽象实现细节，但是需要熟悉其接口：

* `Repository<T, ID extends Serializable>`：标记接口：
    1. 标记管理的持久化对象和ID标志；
    2. 帮助Spring容器发现类路径中带管理的持久化接口；
* `CrudRepository<T, ID extends Serializable>`：抽象所管理持久化对象的CRUD操作；
* `PagingAndSortingRepository<T, ID extends Serializable>`：提供排序和分页支持；
* `QueryDslPredicateExecutor<T>`：不是持久化接口，通过`QueryDsl Predicate`对象获取数据的方式；

Spring Data JPA增加的接口：

* `JpaRepository<T, ID extends Serializable>`：把Spring Data Commons的多个接口合并成一个接口；
* `JpaSpecificationExecutor<T>`：不是持久化接口，通过`Specification<T>`对象从数据库中获取对象；

继承结构如下图：

```
     +----------------------------------------+
     | Repository<T, ID extends Serializable> |
     +-------------------+--------------------+
                        /|\
                         |
                         |
   +--------------------------------------------+ +------------------------------+
   | CrudRepository<T, ID extends Serializable> | | QueryDslPredicateExecutor<T> |
   +---------------------+----------------------+ +------------------------------+
                        /|\
                         |
                         |
+--------------------------------------------------------+
| PagingAndSortingRepository<T, ID extends Serializable> |
+------------------------+-------------------------------+
                        /|\
                         |                               Spring Data Commons
-------------------------+------------------------------------------------------
                         |                                Spring Data JPA
                         |
   +-------------------------------------------+  +------------------------------+
   | JpaRepository<T, ID extends Serializable> |  | JpaSepecificationExecutor<T> |
   +-------------------------------------------+  +------------------------------+
```

Spring Data JPA的工作流程：

1. 创建继承Spring Data的repository interface；
2. 为repository interface添加自定义的查询方法；（可选）
3. 把repository interface插入其他需要的类；

### 依赖包

Spring Data JPA需要以下依赖包：

* JDBC Driver：提供JDBC API，这里使用H2 in-memory database
* Datasource：连接池，如：HikariCP datasource
* JPA Provider：Java Persistence API，如：Hibernate
* Spring Data JPA：隐藏持久化抽象

#### Spring.IO自动引用

启用Spring IO Platform支持

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>io.spring.platform</groupId>
            <artifactId>platform-bom</artifactId>
            <version>1.1.2.RELEASE</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

Spring IO Platform自动引用所需的版本。

```xml
<!-- Database (H2) -->
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
</dependency>
         
<!-- DataSource (HikariCP) -->
<dependency>
    <groupId>com.zaxxer</groupId>
    <artifactId>HikariCP</artifactId>
</dependency>
 
<!-- JPA Provider (Hibernate) -->
<dependency>
    <groupId>org.hibernate</groupId>
    <artifactId>hibernate-entitymanager</artifactId>
</dependency>
 
<!-- Spring Data JPA -->
<dependency>
    <groupId>org.springframework.data</groupId>
    <artifactId>spring-data-jpa</artifactId>
</dependency>
```

#### 手动引用

手动引用依赖包：

```xml
<!-- Database (H2) -->
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <version>1.4.185</version>
</dependency>
         
<!-- DataSource (HikariCP) -->
<dependency>
    <groupId>com.zaxxer</groupId>
    <artifactId>HikariCP</artifactId>
    <version>2.2.5</version>
</dependency>
 
<!-- JPA Provider (Hibernate) -->
<dependency>
    <groupId>org.hibernate</groupId>
    <artifactId>hibernate-entitymanager</artifactId>
    <version>4.3.8.Final</version>
</dependency>
 
<!-- Spring Data JPA -->
<dependency>
    <groupId>org.springframework.data</groupId>
    <artifactId>spring-data-jpa</artifactId>
    <version>1.7.2.RELEASE</version>
</dependency>
```

一般而言，Spring IO Platform自动引用的好处是不需要指定版本，Spring.IO平台会自己照顾版本之间的兼容性。但是如果在老系统中启用Spring Data，一般还是建议使用手工加载引用。

参考：

[petrikainulainen.net](https://www.petrikainulainen.net/programming/spring-framework/spring-data-jpa-tutorial-introduction/)