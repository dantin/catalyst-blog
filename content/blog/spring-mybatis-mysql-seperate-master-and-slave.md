+++
date = "2016-01-13T16:58:36+08:00"
title = "Spring实现MySQL数据库读写分离"
categories = ["Engineering"]
tags = ["Spring", "MySQL", "MyBatis"]
description = "本文记录Spring实现的MySQL读写分离实现"
slug = "spring-mybatis-mysql-seperate-master-and-slave"
+++

通常而言，一个项目只对应一个数据库，基本是一对一的，但是，由于系统负荷逐渐增加，系统就会在数据库的读写上出现瓶颈，读写分离就在这样的大背景下应运而生。

项目中通常使用Spring加Mybatis实现MySQL的主从读写分离，记录如下，供以后参考。

_注意：这种配置是不支持分布式事务的，也就是同一个事务中，不能操作多个数据库。_

高级用法参考[Spring MyBatis多数据源的配置和管理](/blog/spring-mybatis-mysql-multiply-data-source/)。

### 配置

#### 数据源

数据源，通常是server.properties。因为是读写分离，所以需要两个数据源。

``` Bash
jdbc.master.url=jdbc:mysql://10.3.1.241:3306/Azlucky_Frontend?useUnicode=true&amp;characterEncoding=utf-8&amp;\
  zeroDateTimeBehavior=convertToNull&amp;autoReconnect=true
jdbc.slave.url=jdbc:mysql://10.3.1.241:3306/Azlucky_Frontend?useUnicode=true&amp;characterEncoding=utf-8&amp;\
  zeroDateTimeBehavior=convertToNull&amp;autoReconnect=true
jdbc.username=az_fe_dev
jdbc.password=az@fe.dev1
```

#### Spring

文件applicationContext-configuration.xml。

1. 引入数据源配置文件；
2. spring扫描的文件的路径

``` xml
<?xml version="1.0" encoding="UTF-8"?>
<beans
        xmlns="http://www.springframework.org/schema/beans"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:context="http://www.springframework.org/schema/context"
        xmlns:util="http://www.springframework.org/schema/util"
        xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
          http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd
          http://www.springframework.org/schema/util http://www.springframework.org/schema/util/spring-util.xsd">

    <!-- Enable annotation based container configuration  -->
    <context:annotation-config/>

    <!-- 使用annotation 自动注册bean,并保证@Required,@Autowired的属性被注入 -->
    <context:component-scan base-package="com.aztechx.search.indexer"/>

    <context:property-placeholder location="classpath:server.properties" ignore-unresolvable="true"/>
</beans>
```

文件applicationContext-dataSource.xml。

``` xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:tx="http://www.springframework.org/schema/tx"
       xmlns:aop="http://www.springframework.org/schema/aop"
       xsi:schemaLocation="
        http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.1.xsd
        http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx-3.1.xsd
        http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop-3.0.xsd">

    <description>数据源配置</description>

    <!-- 数据源配置,使用应用内的DBCP数据库连接池 -->
    <bean id="masterDataSourceImpl" class="org.apache.commons.dbcp.BasicDataSource" destroy-method="close">
        <!-- Connection Info -->
        <property name="driverClassName" value="${jdbc.driver}"/>
        <property name="url" value="${jdbc.master.url}"/>
        <property name="username" value="${jdbc.username}"/>
        <property name="password" value="${jdbc.password}"/>
        <!-- Connection Pooling Info -->
        <!-- 连接池中最多可空闲maxIdle个连接 -->
        <property name="maxIdle" value="${dbcp.maxIdle}"/>
        <!-- 连接池支持的最大连接数 -->
        <property name="maxActive" value="${dbcp.maxActive}"/>
        <!-- 连接池中连接用完时,新的请求等待时间,毫秒 -->
        <property name="maxWait" value="${dbcp.maxWait}"/>
        <property name="defaultAutoCommit" value="false"/>
        <!-- 是否自动回收超时连接 -->
        <property name="removeAbandoned" value="true"/>
        <!-- 超时时间(以秒数为单位) -->
        <property name="removeAbandonedTimeout" value="${dbcp.removeAbandonedTimeout}"/>
        <!-- 在回收事件后，在log中打印出回收Connection的错误信息，包括在哪个地方用了Connection却忘记关闭了，在调试的时候很有用 -->
        <property name="logAbandoned" value="true"/>
        <property name="poolPreparedStatements" value="true"/>
        <!-- 每timeBetweenEvictionRunsMillis毫秒检查一次连接池中空闲的连接,把空闲时间超过minEvictableIdleTimeMillis毫秒的连接
        断开,直到连接池中的连接数到minIdle为止 -->
        <property name="timeBetweenEvictionRunsMillis" value="${dbcp.timeBetweenEvictionRunsMillis}"/>
        <!-- 连接池中连接可空闲的时间(毫秒)，一定要小于mysql的wait_timeout的值 -->
        <property name="minEvictableIdleTimeMillis" value="${dbcp.minEvictableIdleTimeMillis}"/>
        <!-- 返回连接时验证其有效性 -->
        <property name="testOnReturn" value="false"/>
        <!-- 指明连接是否被空闲连接回收器(如果有)进行检验.如果检测失败,则连接将被从池中去除 -->
        <property name="testWhileIdle" value="true"/>
        <!-- 取得连接时验证其有效性 -->
        <property name="testOnBorrow" value="false"/>
        <!-- 验证SQL -->
        <property name="validationQuery" value="select 1"/>
    </bean>

    <!-- 线上从库的数据源 -->
    <bean id="slaveDataSourceImpl" class="org.apache.commons.dbcp.BasicDataSource"
          destroy-method="close">
        <property name="driverClassName" value="${jdbc.driver}"/>
        <property name="url" value="${jdbc.slave.url}"/>
        <property name="username" value="${jdbc.username}"/>
        <property name="password" value="${jdbc.password}"/>
        <property name="maxIdle" value="${dbcp.maxIdle}"/>
        <property name="maxActive" value="${dbcp.maxActive}"/>
        <property name="maxWait" value="${dbcp.maxWait}"/>
        <property name="defaultAutoCommit" value="false"/>
        <property name="removeAbandoned" value="true"/>
        <property name="removeAbandonedTimeout" value="${dbcp.removeAbandonedTimeout}"/>
        <property name="logAbandoned" value="true"/>
        <property name="poolPreparedStatements" value="true"/>
        <property name="timeBetweenEvictionRunsMillis" value="${dbcp.timeBetweenEvictionRunsMillis}"/>
        <property name="minEvictableIdleTimeMillis" value="${dbcp.minEvictableIdleTimeMillis}"/>
        <property name="testOnReturn" value="false"/>
        <property name="testWhileIdle" value="true"/>
        <property name="testOnBorrow" value="false"/>
        <property name="validationQuery" value="select 1"/>
    </bean>

    <!-- DataSource/Master -->
    <bean id="masterDataSource"
          class="org.springframework.jdbc.datasource.TransactionAwareDataSourceProxy">
        <property name="targetDataSource" ref="masterDataSourceImpl"/>
    </bean>
    <bean id="masterTransactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
        <property name="dataSource" ref="masterDataSource"/>
    </bean>
    <bean id="masterTransactionTemplate"
          class="org.springframework.transaction.support.TransactionTemplate">
        <property name="transactionManager" ref="masterTransactionManager"/>
    </bean>

    <!-- DataSource/Slave -->
    <bean id="slaveDataSource" class="org.springframework.jdbc.datasource.TransactionAwareDataSourceProxy">
        <property name="targetDataSource" ref="slaveDataSourceImpl"/>
    </bean>
    <bean id="slaveTransactionManager"
          class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
        <property name="dataSource" ref="slaveDataSource"/>
    </bean>
    <bean id="slaveTransactionTemplate"
          class="org.springframework.transaction.support.TransactionTemplate">
        <property name="transactionManager" ref="slaveTransactionManager"/>
    </bean>

    <!-- Mybatis/Master -->
    <bean id="masterSqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
        <property name="dataSource" ref="masterDataSource"/>
        <property name="configLocation" value="classpath:/mapper/Configuration.xml"/>
        <property name="mapperLocations" value="classpath:/mapper/*MasterMapper.xml"/>
    </bean>

    <bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">
        <property name="addToConfig" value="true"/>
        <property name="basePackage" value="com.aztechx.search.indexer.smarter.dao.mapper.master"/>
        <property name="sqlSessionFactoryBeanName" value="masterSqlSessionFactory"/>
    </bean>


    <!-- Mybatis/Slave -->
    <bean id="slaveSqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
        <property name="dataSource" ref="slaveDataSource"/>
        <property name="configLocation" value="classpath:/mapper/Configuration.xml"/>
        <property name="mapperLocations" value="classpath:/mapper/*SlaveMapper.xml"/>
    </bean>

    <bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">
        <property name="addToConfig" value="true"/>
        <property name="basePackage" value="com.aztechx.search.indexer.smarter.dao.mapper.slave"/>
        <property name="sqlSessionFactoryBeanName" value="slaveSqlSessionFactory"/>
    </bean>

    <!-- Configuration transaction advice -->
    <tx:advice id="txAdvice" transaction-manager="masterTransactionManager">
        <tx:attributes>
            <tx:method name="add*" propagation="REQUIRED"/>
            <tx:method name="update*" propagation="REQUIRED"/>
            <tx:method name="delete*" propagation="REQUIRED"/>
            <tx:method name="get*" read-only="true" propagation="SUPPORTS"/>
            <tx:method name="list*" read-only="true" propagation="SUPPORTS"/>
        </tx:attributes>
    </tx:advice>

    <!-- Configuration transaction aspect -->
    <aop:config>
        <aop:pointcut id="systemServicePointcut"
                      expression="execution(* com.aztechx.search.indexer.smarter.service.*.*(..))"/>
        <aop:advisor advice-ref="txAdvice" pointcut-ref="systemServicePointcut"/>
    </aop:config>

</beans>
```

这里需要注意的是：

1. com.aztechx.search.indexer.smarter.dao.mapper.master包中的接口写主库
2. com.aztechx.search.indexer.smarter.dao.mapper.slave包中的接口读从库

最后通过AOP实现了事务。

#### Mybatis

Mybatis的配置文件Configuration.xml

``` xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">

<configuration>
    <settings>
        <setting name="cacheEnabled" value="true" />
        <setting name="lazyLoadingEnabled" value="true" />
    </settings>
</configuration>
```

#### 依赖包

由于使用了AOP，因此需要引入AspectJ。

``` xml
<!-- AspectJ -->
<dependency>
    <groupId>org.aspectj</groupId>
    <artifactId>aspectjrt</artifactId>
    <version>${aspectj.version}</version>
</dependency>
<dependency>
    <groupId>org.aspectj</groupId>
    <artifactId>aspectjweaver</artifactId>
    <version>${aspectj.version}</version>
</dependency>
```

以上。

参考

* [自定义的读写分离](http://www.cnblogs.com/xiaochangwei/p/4961807.html)
* [多数据源的读写分离](http://www.bridgeli.cn/archives/166)
* [多数据源的配置和使用](http://kingxss.iteye.com/blog/1620314)