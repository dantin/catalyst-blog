+++
date = "2016-04-14T11:24:49+08:00"
title = "Spring MyBatis多数据源的配置和管理"
categories = ["Engineering"]
tags = ["Spring", "MySQL", "MyBatis"]
description = "本文记录Spring对MySQL多数据源的支持"
slug = "spring-mybatis-mysql-multiply-data-source"
+++

本文记录多数据源的配置和管理方案。

### 多数源现状

同一个项目有时会涉及到多个数据库，也就是多数据源。多数据源又可以分为两种情况：

1. 两个或多个数据库没有相关性，各自独立，其实这种可以作为两个项目来开发。比如在游戏开发中一个数据库是平台数据库，其它还有平台下的游戏对应的数据库；

2. 两个或多个数据库是Master-Slave的关系，比如有MySQL搭建一个Master-Master，其后又带有多个Slave；或者采用MHA搭建的Master-Slave复制；

目前Spring多数据源的搭建大概有两种方式，可以根据多数据源的情况进行选择。

### 采用Spring配置文件直接配置多个数据源

比如针对两个数据库没有相关性的情况，可以采用直接在spring的配置文件中配置多个数据源，然后分别进行事务的配置，如下所示：

```xml
<context:component-scan base-package="net.aazj.service,net.aazj.aop" />
    <context:component-scan base-package="net.aazj.aop" />
    <!-- 引入属性文件 -->
    <context:property-placeholder location="classpath:config/db.properties" />

    <!-- 配置数据源 -->
    <bean name="dataSource" class="com.alibaba.druid.pool.DruidDataSource" init-method="init" destroy-method="close">
        <property name="url" value="${jdbc_url}" />
        <property name="username" value="${jdbc_username}" />
        <property name="password" value="${jdbc_password}" />
        <!-- 初始化连接大小 -->
        <property name="initialSize" value="0" />
        <!-- 连接池最大使用连接数量 -->
        <property name="maxActive" value="20" />
        <!-- 连接池最大空闲 -->
        <property name="maxIdle" value="20" />
        <!-- 连接池最小空闲 -->
        <property name="minIdle" value="0" />
        <!-- 获取连接最大等待时间 -->
        <property name="maxWait" value="60000" />
    </bean>
    
    <bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
      <property name="dataSource" ref="dataSource" />
      <property name="configLocation" value="classpath:config/mybatis-config.xml" />
      <property name="mapperLocations" value="classpath*:config/mappers/**/*.xml" />
    </bean>
    
    <!-- Transaction manager for a single JDBC DataSource -->
    <bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
        <property name="dataSource" ref="dataSource" />
    </bean>
    
    <!-- 使用annotation定义事务 -->
    <tx:annotation-driven transaction-manager="transactionManager" /> 
    
    <bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">
      <property name="basePackage" value="net.aazj.mapper" />
      <property name="sqlSessionFactoryBeanName" value="sqlSessionFactory"/>
    </bean>

    <!-- Enables the use of the @AspectJ style of Spring AOP -->
    <aop:aspectj-autoproxy/>
    
    <!-- ===============第二个数据源的配置=============== -->
    <bean name="dataSource_2" class="com.alibaba.druid.pool.DruidDataSource" init-method="init" destroy-method="close">
        <property name="url" value="${jdbc_url_2}" />
        <property name="username" value="${jdbc_username_2}" />
        <property name="password" value="${jdbc_password_2}" />
        <!-- 初始化连接大小 -->
        <property name="initialSize" value="0" />
        <!-- 连接池最大使用连接数量 -->
        <property name="maxActive" value="20" />
        <!-- 连接池最大空闲 -->
        <property name="maxIdle" value="20" />
        <!-- 连接池最小空闲 -->
        <property name="minIdle" value="0" />
        <!-- 获取连接最大等待时间 -->
        <property name="maxWait" value="60000" />
    </bean>
    
    <bean id="sqlSessionFactory_slave" class="org.mybatis.spring.SqlSessionFactoryBean">
      <property name="dataSource" ref="dataSource_2" />
      <property name="configLocation" value="classpath:config/mybatis-config-2.xml" />
      <property name="mapperLocations" value="classpath*:config/mappers2/**/*.xml" />
    </bean>
    
    <!-- Transaction manager for a single JDBC DataSource -->
    <bean id="transactionManager_2" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
        <property name="dataSource" ref="dataSource_2" />
    </bean>
    
    <!-- 使用annotation定义事务 -->
    <tx:annotation-driven transaction-manager="transactionManager_2" /> 
    
    <bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">
      <property name="basePackage" value="net.aazj.mapper2" />
      <property name="sqlSessionFactoryBeanName" value="sqlSessionFactory_2"/>
    </bean>
```

如上所示，我们分别配置了两个dataSource，两个sqlSessionFactory，两个transactionManager，以及关键的地方在于MapperScannerConfigurer的配置－－使用__sqlSessionFactoryBeanName__属性，注入不同的sqlSessionFactory的名称，这样的话，就为不同的数据库对应的mapper接口注入了对应的sqlSessionFactory。

_需要注意的是，多个数据库的这种配置是不支持分布式事务的，也就是同一个事务中，不能操作多个数据库。_这种配置方式的优点是很简单，但是却不灵活。对于Master-Slave类型的多数据源配置而言不太适应，Master-Slave性的多数据源的配置，需要特别灵活，需要根据业务的类型进行细致的配置。比如对于一些耗时特别大的SELECT语句，我们希望放到Slave上执行，而对于UPDATE, DELETE等操作肯定是只能在Master上执行的，另外对于一些实时性要求很高的SELECT语句，我们也可能需要放到Master上执行——比如一个场景是我去商城购买一件兵器，购买操作的很定是Master，同时购买完成之后，需要重新查询出我所拥有的兵器和金币，那么这个查询可能也需要防止Master上执行，而不能放在Slave上去执行，因为Slave上可能存在延时，我们可不希望玩家发现购买成功之后，在背包中却找不到兵器的情况出现。

所以对于Master-Slave类型的多数据源的配置，需要根据业务来进行灵活的配置，哪些SELECT可以放到Slave上，哪些SELECT不能放到Slave上。所以上面的那种所数据源的配置就不太适应了。

### 基于AbstractRoutingDataSource和AOP的多数据源的配置

基本原理是，我们自己定义一个DataSource类ThreadLocalRoutingDataSource，来继承AbstractRoutingDataSource，然后在配置文件中向ThreadLocalRountingDataSource注入Master和Slave的数据源，然后通过AOP来灵活配置，在哪些地方选择Master数据源，在哪些地方需要选择Slave数据源。下面看代码实现：

#### 区分数据源

先定义一个enum来表示不同的数据源

```java
package net.aazj.enums;

/**
 * 数据源的类别：master/slave
 */
public enum DataSources {
    MASTER, SLAVE
}
```

#### 定义标志位

通过TheadLocal来保存每个线程选择哪个数据源的标志(key)

```java
package net.aazj.util;

import net.aazj.enums.DataSources;

public class DataSourceTypeManager {
    private static final ThreadLocal<DataSources> dataSourceTypes = new ThreadLocal<DataSources>(){
        @Override
        protected DataSources initialValue(){
            return DataSources.MASTER;
        }
    };
    
    public static DataSources get(){
        return dataSourceTypes.get();
    }
    
    public static void set(DataSources dataSourceType){
        dataSourceTypes.set(dataSourceType);
    }
    
    public static void reset(){
        dataSourceTypes.set(DataSources.MASTER);
    }
}
```

#### 自定义DataSource

定义ThreadLocalRountingDataSource，继承AbstractRoutingDataSource

```java
package net.aazj.util;

import org.springframework.jdbc.datasource.lookup.AbstractRoutingDataSource;

public class ThreadLocalRountingDataSource extends AbstractRoutingDataSource {
    @Override
    protected Object determineCurrentLookupKey() {
        return DataSourceTypeManager.get();
    }
}
```

#### 配置

在配置文件中向ThreadLocalRountingDataSource注入Master和Slave的数据源

```xml
<context:component-scan base-package="net.aazj.service,net.aazj.aop" />
<context:component-scan base-package="net.aazj.aop" />
<!-- Enables the use of the @AspectJ style of Spring AOP -->
<aop:aspectj-autoproxy/>
<!-- 引入属性文件 -->
<context:property-placeholder location="classpath:config/db.properties" />    
<!-- 配置数据源Master -->
<bean name="dataSourceMaster" class="com.alibaba.druid.pool.DruidDataSource" init-method="init" des-method="close">
    <property name="url" value="${jdbc_url}" />
    <property name="username" value="${jdbc_username}" />
    <property name="password" value="${jdbc_password}" />
    <!-- 初始化连接大小 -->
    <property name="initialSize" value="0" />
    <!-- 连接池最大使用连接数量 -->
    <property name="maxActive" value="20" />
    <!-- 连接池最大空闲 -->
    <property name="maxIdle" value="20" />
    <!-- 连接池最小空闲 -->
    <property name="minIdle" value="0" />
    <!-- 获取连接最大等待时间 -->
    <property name="maxWait" value="60000" />
</bean>    
<!-- 配置数据源Slave -->
<bean name="dataSourceSlave" class="com.alibaba.druid.pool.DruidDataSource" init-method="init" destmethod="close">
    <property name="url" value="${jdbc_url_slave}" />
    <property name="username" value="${jdbc_username_slave}" />
    <property name="password" value="${jdbc_password_slave}" />
    <!-- 初始化连接大小 -->
    <property name="initialSize" value="0" />
    <!-- 连接池最大使用连接数量 -->
    <property name="maxActive" value="20" />
    <!-- 连接池最大空闲 -->
    <property name="maxIdle" value="20" />
    <!-- 连接池最小空闲 -->
    <property name="minIdle" value="0" />
    <!-- 获取连接最大等待时间 -->
    <property name="maxWait" value="60000" />
</bean>    
<bean id="dataSource" class="net.aazj.util.ThreadLocalRountingDataSource">
    <property name="defaultTargetDataSource" ref="dataSourceMaster" />
    <property name="targetDataSources">
        <map key-type="net.aazj.enums.DataSources">
            <entry key="MASTER" value-ref="dataSourceMaster"/>
            <entry key="SLAVE" value-ref="dataSourceSlave"/>
            <!-- 这里还可以加多个dataSource -->
        </map>
    </property>
</bean>    
<bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
  <property name="dataSource" ref="dataSource" />
  <property name="configLocation" value="classpath:config/mybatis-config.xml" />
  <property name="mapperLocations" value="classpath*:config/mappers/**/*.xml" />
</bean>    
<!-- Transaction manager for a single JDBC DataSource -->
<bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
    <property name="dataSource" ref="dataSource" />
</bean>    
<!-- 使用annotation定义事务 -->
<tx:annotation-driven transaction-manager="transactionManager" /> 
<bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">
  <property name="basePackage" value="net.aazj.mapper" />
  <!-- <property name="sqlSessionFactoryBeanName" value="sqlSessionFactory"/> -->
</bean>
```

上面spring的配置文件中，我们针对Master数据库和Slave数据库分别定义了dataSourceMaster和dataSourceSlave两个dataSource，然后注入到<bean id="dataSource" class="net.aazj.util.ThreadLocalRountingDataSource"> 中，这样我们的dataSource就可以来根据key的不同来选择dataSourceMaster和dataSourceSlave了。

#### AOP

使用Spring AOP来指定dataSource的key，从而dataSource会根据key选择dataSourceMaster和dataSourceSlave

```java
package net.aazj.aop;

import net.aazj.enums.DataSources;
import net.aazj.util.DataSourceTypeManager;

import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.stereotype.Component;

@Aspect    // for aop
@Component // for auto scan
@Order(0)  // execute before @Transactional
public class DataSourceInterceptor {    
    @Pointcut("execution(public * net.aazj.service..*.getUser(..))")
    public void dataSourceSlave(){};
    
    @Before("dataSourceSlave()")
    public void before(JoinPoint jp) {
        DataSourceTypeManager.set(DataSources.SLAVE);
    }
    // ... ...
}
```

这里我们定义了一个Aspect类，使用@Before来在符合@Pointcut("execution(public * net.aazj.service..*.getUser(..))")中的方法被调用之前，调用DataSourceTypeManager.set(DataSources.SLAVE)设置了key的类型为 DataSources.SLAVE，所以dataSource会根据key=DataSources.SLAVE选择dataSourceSlave这个dataSource。所以该方法对于的sql语句会在slave数据库上执行(注意：这里存在多个Aspect之间的一个执行顺序的问题，必须保证切换数据源的Aspect必须在@Transactional这个Aspect之前执行，所以这里使用了@Order(0)来保证切换数据源先于@Transactional执行)。

我们可以不断的扩充DataSourceInterceptor这个Aspect，在中进行各种各样的定义，来为某个service的某个方法指定合适的数据源对应的dataSource。

这样我们就可以使用 Spring AOP 的强大功能来，十分灵活进行配置了。

#### 原理剖析

AbstractRoutingDataSource原理剖析

ThreadLocalRountingDataSource继承了AbstractRoutingDataSource，实现其抽象方法protected abstract Object determineCurrentLookupKey(); 从而实现对不同数据源的路由功能。

我们从源码入手分析下其中原理：

```java
public abstract class AbstractRoutingDataSource extends AbstractDataSource implements InitializingBean
```

AbstractRoutingDataSource实现了InitializingBean，那么Spring在初始化该Bean时，会调用InitializingBean的接口
void afterPropertiesSet() throws Exception; 我们看下AbstractRoutingDataSource是如何实现这个接口的。

```java
@Override
public void afterPropertiesSet() {
    if (this.targetDataSources == null) {
        throw new IllegalArgumentException("Property 'targetDataSources' is required");
    }
    this.resolvedDataSources = new HashMap<Object, DataSource>(this.targetDataSources.size());
    for (Map.Entry<Object, Object> entry : this.targetDataSources.entrySet()) {
        Object lookupKey = resolveSpecifiedLookupKey(entry.getKey());
        DataSource dataSource = resolveSpecifiedDataSource(entry.getValue());
        this.resolvedDataSources.put(lookupKey, dataSource);
    }
    if (this.defaultTargetDataSource != null) {
        this.resolvedDefaultDataSource = resolveSpecifiedDataSource(this.defaultTargetDataSource);
    }
}
```

targetDataSources是我们在xml配置文件中注入的dataSourceMaster和dataSourceSlave。afterPropertiesSet方法就是使用注入的dataSourceMaster和dataSourceSlave来构造一个HashMap－－resolvedDataSources。方便后面根据key从该map中取得对应的dataSource。

我们再看下AbstractDataSource接口中的Connection getConnection() throws SQLException;是如何实现的。

```java
@Override
public Connection getConnection() throws SQLException {
    return determineTargetDataSource().getConnection();
}
```

关键在于determineTargetDataSource()，根据方法名就可以看出，应该此处就决定了使用哪个dataSource。

```java
protected DataSource determineTargetDataSource() {
    Assert.notNull(this.resolvedDataSources, "DataSource router not initialized");
    Object lookupKey = determineCurrentLookupKey();
    DataSource dataSource = this.resolvedDataSources.get(lookupKey);
    if (dataSource == null && (this.lenientFallback || lookupKey == null)) {
        dataSource = this.resolvedDefaultDataSource;
    }
    if (dataSource == null) {
        throw new IllegalStateException("Cannot determine target DataSource for lookup key [lookupKey + "]");
    }
    return dataSource;
}
```

Object lookupKey = determineCurrentLookupKey();该方法是我们实现的，在其中获取ThreadLocal中保存的key值。

获得了key之后，在从afterPropertiesSet()中初始化好了的resolvedDataSources这个map中获得key对应的dataSource。而ThreadLocal中保存的key值是通过AOP的方式在调用service中相关方法之前设置好的。

OK，到此搞定！

#### 扩展

扩展ThreadLocalRountingDataSource

上面我们只是实现了Master-Slave数据源的选择。如果有多台Master或者有多台Slave。多台Master组成一个HA，要实现当其中一台master挂了时，自动切换到另一台Master，这个功能可以使用LVS/Keepalived来实现，也可以通过进一步扩展ThreadLocalRountingDataSource来实现，可以另外加一个线程专门来每个一秒来测试MySQL是否正常来实现。

同样对于多台Slave之间要实现负载均衡，同时当一台slave挂了时，要实现将其从负载均衡中去除掉，这个功能既可以使用LVS/Keepalived来实现，同样也可以通过近一步扩展ThreadLocalRountingDataSource来实现。

### 总结

从本文中我们可以体会到AOP的强大和灵活。

本文使用的是mybatis,其实使用Hibernate也应该是相似的配置。

参考

[Bigdeep](http://www.cnblogs.com/digdeep/p/4512368.html)