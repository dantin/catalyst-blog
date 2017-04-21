+++
slug = "springboot-mybatis-sharding-jdbc"
date = "2017-04-21T11:21:40+08:00"
title = "基于sharding-jdbc的分库分表方法"
categories = ["Engineering"]
tags = ["SpringBoot", "MyBatis", "MySQL"]
description = "本文记录基于sharding-jdbc的分库分表方法"
+++

[Sharding-jdbc](https://github.com/dangdangdotcom/sharding-jdbc)当当开源的一个分库分表方案，和阿里开源的[Cobar](https://github.com/alibaba/cobar)不同，sharding-jdbc不需要另外的Proxy中间件；与阿里半开源的[TDDL](https://github.com/alibaba/tb_tddl)不同，sharding-jdbc不强依赖diamond（配置中心）。

### 系统架构

sharding-jdbc的工作原理如下：

<img src="/images/sharding-jdbc.png" alt="架构" style="width: 500px;"/>

其核心在于对SQL的解析处理和对操作结果的合并。

### 示例

下面以一个例子做demo看一下sharding-jdbc的使用。

业务场景如下：

A、B两个工厂在上海，深圳，需要实时记录这两两个工厂的所有交易order。现在的分片策略是：上海、深圳分别建库，每个库都存各自的订单，且按照月分表。如图：

```console
db sh

   order_a_2017_04
   order_b_2017_05
   ... ...
   order_a_2017_04
   order_b_2017_05

db_sz

   order_a_2017_04
   order_b_2017_05
   ... ...
   order_a_2017_04
   order_b_2017_05
```

分库分表就是这样的。根据这个建库。

Sharding-jdbc是不支持建库的SQL，如果需要增量的数据库和数据表，那就要一次性把一段时期的数据库和数据表都要建好。

#### 建库

SQL语句如下

```sql
DROP DATABASE IF EXISTS db_sh;
DROP TABLE IF EXISTS db_sh.orders_a_2017_04;
CREATE TABLE db_sh.orders_a_2017_04
(
  id BIGINT(20) PRIMARY KEY NOT NULL,
  name VARCHAR(2),
  exchange VARCHAR(10),
  ask INT(11),
  bid INT(11),
  time DATETIME
);
DROP TABLE IF EXISTS db_sh.orders_a_2017_05;
CREATE TABLE db_sh.orders_a_2017_05
(
  id BIGINT(20) PRIMARY KEY NOT NULL,
  name VARCHAR(2),
  exchange VARCHAR(10),
  ask INT(11),
  bid INT(11),
  time DATETIME
);
DROP TABLE IF EXISTS db_sh.orders_b_2017_04;
CREATE TABLE db_sh.orders_b_2017_04
(
  id BIGINT(20) PRIMARY KEY NOT NULL,
  name VARCHAR(2),
  exchange VARCHAR(10),
  ask INT(11),
  bid INT(11),
  time DATETIME
);
DROP TABLE IF EXISTS db_sh.orders_b_2017_05;
CREATE TABLE db_sh.orders_b_2017_05
(
  id BIGINT(20) PRIMARY KEY NOT NULL,
  name VARCHAR(2),
  exchange VARCHAR(10),
  ask INT(11),
  bid INT(11),
  time DATETIME
);
DROP DATABASE IF EXISTS db_sz;
DROP TABLE IF EXISTS db_sz.orders_a_2017_04;
CREATE TABLE db_sz.orders_a_2017_04
(
  id BIGINT(20) PRIMARY KEY NOT NULL,
  name VARCHAR(2),
  exchange VARCHAR(10),
  ask INT(11),
  bid INT(11),
  time DATETIME
);
DROP TABLE IF EXISTS db_sz.orders_a_2017_05;
CREATE TABLE db_sz.orders_a_2017_05
(
  id BIGINT(20) PRIMARY KEY NOT NULL,
  name VARCHAR(2),
  exchange VARCHAR(10),
  ask INT(11),
  bid INT(11),
  time DATETIME
);
DROP TABLE IF EXISTS db_sz.orders_b_2017_04;
CREATE TABLE db_sz.orders_b_2017_04
(
  id BIGINT(20) PRIMARY KEY NOT NULL,
  name VARCHAR(2),
  exchange VARCHAR(10),
  ask INT(11),
  bid INT(11),
  time DATETIME
);
DROP TABLE IF EXISTS db_sz.orders_b_2017_05;
CREATE TABLE db_sz.orders_b_2017_05
(
  id BIGINT(20) PRIMARY KEY NOT NULL,
  name VARCHAR(2),
  exchange VARCHAR(10),
  ask INT(11),
  bid INT(11),
  time DATETIME
);
```

#### 集成springboot和sharding-jdbc

POM.xml如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.cosmos</groupId>
    <artifactId>springboot-sharding-jdbc-demo</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>1.5.2.RELEASE</version>
    </parent>

    <properties>
        <!-- Overrides to parent POM -->
        <java.version>1.8</java.version>

        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <project.build.jdk>${java.version}</project.build.jdk>

        <sharding-jdbc.version>1.4.2</sharding-jdbc.version>
    </properties>

    <dependencies>
        <!-- spring boot -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-jdbc</artifactId>
        </dependency>
        <!-- sharding-jdbc -->
        <dependency>
            <groupId>com.dangdang</groupId>
            <artifactId>sharding-jdbc-core</artifactId>
            <version>${sharding-jdbc.version}</version>
        </dependency>
        <dependency>
            <groupId>com.dangdang</groupId>
            <artifactId>sharding-jdbc-config-spring</artifactId>
            <version>${sharding-jdbc.version}</version>
        </dependency>
        <dependency>
            <groupId>com.dangdang</groupId>
            <artifactId>sharding-jdbc-self-id-generator</artifactId>
            <version>${sharding-jdbc.version}</version>
        </dependency>
        <!-- druid -->
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>druid</artifactId>
            <version>1.0.18</version>
        </dependency>
        <!-- mysql -->
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <scope>runtime</scope>
        </dependency>
        <!-- mybatis -->
        <dependency>
            <groupId>org.mybatis</groupId>
            <artifactId>mybatis</artifactId>
            <version>3.4.4</version>
        </dependency>
        <dependency>
            <groupId>org.mybatis</groupId>
            <artifactId>mybatis-spring</artifactId>
            <version>1.3.1</version>
        </dependency>
        <!-- tool -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
        </dependency>

        <!-- test -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <version>1.5.2.RELEASE</version>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.1</version>
                <configuration>
                    <source>${project.build.jdk}</source>
                    <target>${project.build.jdk}</target>
                    <encoding>${project.build.sourceEncoding}</encoding>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>2.4</version>
            </plugin>
        </plugins>
    </build>

</project>
```

#### 配置数据源

数据库连接记录在`application.yml`

```console
server:
  port: 9120

jdbc:
  driver-class-name: com.mysql.jdbc.Driver

database:
  source:
    sh:
      url: jdbc:mysql://127.0.0.1:3306/db_sh?useUnicode=true&autoReconnect=true&rewriteBatchedStatements=true
      username: root
      password: root
    sz:
      url: jdbc:mysql://127.0.0.1:3306/db_sz?useUnicode=true&autoReconnect=true&rewriteBatchedStatements=true
      username: root
      password: root
```

sharding-jdbc的原理其实很简单，就是自己做一个DataSource给上层应用使用，这个DataSource包含所有的逻辑库和逻辑表，应用增删改查时，他自己再修改sql，然后选择合适的数据库继续操作。所以这个DataSource创建很重要。

```java
import com.alibaba.druid.pool.DruidDataSource;
import com.dangdang.ddframe.rdb.sharding.api.ShardingDataSourceFactory;
import com.dangdang.ddframe.rdb.sharding.api.rule.DataSourceRule;
import com.dangdang.ddframe.rdb.sharding.api.rule.ShardingRule;
import com.dangdang.ddframe.rdb.sharding.api.rule.TableRule;
import com.dangdang.ddframe.rdb.sharding.api.strategy.database.DatabaseShardingStrategy;
import com.dangdang.ddframe.rdb.sharding.api.strategy.table.TableShardingStrategy;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.core.env.Environment;

import javax.sql.DataSource;
import java.util.Arrays;
import java.util.HashMap;

@Configuration
@Slf4j
public class DataSourceConfig {

    private final Environment env;

    @Autowired
    public DataSourceConfig(Environment env) {
        this.env = env;
    }

    @Bean(name = "db_sh")
    public DataSource masterDataSource1() {
        DruidDataSource druidDataSource = new DruidDataSource();
        druidDataSource.setDriverClassName(env.getProperty("jdbc.driverClassName"));
        druidDataSource.setUrl(env.getProperty("database.source.sh.url"));
        druidDataSource.setUsername(env.getProperty("database.source.sh.username"));
        druidDataSource.setPassword(env.getProperty("database.source.sh.password"));
        log.info("DB [SH]: {}", env.getProperty("database.source.sh.url"));
        return druidDataSource;
    }

    @Bean(name = "db_sz")
    public DataSource masterDataSource2() {
        DruidDataSource druidDataSource = new DruidDataSource();
        druidDataSource.setDriverClassName(env.getProperty("jdbc.driverClassName"));
        druidDataSource.setUrl(env.getProperty("database.source.sz.url"));
        druidDataSource.setUsername(env.getProperty("database.source.sz.username"));
        druidDataSource.setPassword(env.getProperty("database.source.sz.password"));
        log.info("DB [SZ]: {}", env.getProperty("database.source.sz.url"));
        return druidDataSource;
    }

    @Bean
    public HashMap<String, DataSource> dataSourceMap(
            @Qualifier("db_sh") DataSource dataSource1,
            @Qualifier("db_sz") DataSource dataSource2) {
        HashMap<String, DataSource> dataSourceMap = new HashMap<>();
        dataSourceMap.put("db_sh", dataSource1);
        dataSourceMap.put("db_sz", dataSource2);
        return dataSourceMap;
    }
    
    @Bean
    @Primary
    public DataSource shardingDataSource(
            HashMap<String, DataSource> dataSourceMap,
            DatabaseShardingStrategy databaseShardingStrategy,
            TableShardingStrategy tableShardingStrategy) {
        DataSourceRule dataSourceRule = new DataSourceRule(dataSourceMap);
        TableRule tableRule = TableRule.builder("orders")
                .actualTables(Arrays.asList("db_sh.orders_a_2017_04", "db_sh.orders_a_2017_05", "db_sh.orders_b_2017_04", "db_sh.orders_b_2017_05", "db_sz.orders_a_2017_04", "db_sz.orders_a_2017_05", "db_sz.orders_b_2017_04", "db_sz.orders_a_2017_05"))
                .dataSourceRule(dataSourceRule)
                .build();
        ShardingRule shardingRule = ShardingRule.builder()
                .dataSourceRule(dataSourceRule)
                .tableRules(Arrays.asList(tableRule))
                .databaseShardingStrategy(databaseShardingStrategy)
                .tableShardingStrategy(tableShardingStrategy)
                .build();
        return ShardingDataSourceFactory.createDataSource(shardingRule);
    }

}
```
这里要着重说一下为什么要用`@Primary`这个注解，没有这个注解是会报错的，错误大致意思就是DataSource太多了，MyBatis不知道用哪个。加上这个MyBatis就知道用sharding的DataSource了。

这样就把各个逻辑数据库就加载好了。

#### 配置分片策略

__数据库分片__

在这个实例中，数据库的分库就是根据上海(sh)和深圳(sz)来分的，在sharding-jdbc中是单键分片。根据官方文档实现接口 SingleKeyDatabaseShardingAlgorithm 就可以

```java
import com.dangdang.ddframe.rdb.sharding.api.ShardingValue;
import com.dangdang.ddframe.rdb.sharding.api.strategy.database.SingleKeyDatabaseShardingAlgorithm;
import org.springframework.stereotype.Component;

import java.util.Collection;

@Component
public class DatabaseShardingAlgorithm implements SingleKeyDatabaseShardingAlgorithm<String> {

    /**
     * 根据分片值和SQL的=运算符计算分片结果名称集合.
     *
     * @param availableTargetNames 所有的可用目标名称集合, 一般是数据源或表名称
     * @param shardingValue        分片值
     * @return 分片后指向的目标名称, 一般是数据源或表名称
     */
    @Override
    public String doEqualSharding(Collection<String> availableTargetNames, ShardingValue<String> shardingValue) {
        String databaseName = "";
        for (String targetName : availableTargetNames) {
            if (targetName.endsWith(shardingValue.getValue())) {
                databaseName = targetName;
                break;
            }
        }
        return databaseName;
    }

    /**
     * 根据分片值和SQL的IN运算符计算分片结果名称集合.
     *
     * @param availableTargetNames 所有的可用目标名称集合, 一般是数据源或表名称
     * @param shardingValue        分片值
     * @return 分片后指向的目标名称集合, 一般是数据源或表名称
     */
    @Override
    public Collection<String> doInSharding(Collection<String> availableTargetNames, ShardingValue<String> shardingValue) {
        return null;
    }

    /**
     * 根据分片值和SQL的BETWEEN运算符计算分片结果名称集合.
     *
     * @param availableTargetNames 所有的可用目标名称集合, 一般是数据源或表名称
     * @param shardingValue        分片值
     * @return 分片后指向的目标名称集合, 一般是数据源或表名称
     */
    @Override
    public Collection<String> doBetweenSharding(Collection<String> availableTargetNames, ShardingValue<String> shardingValue) {
        return null;
    }
}
```

此接口还有另外两个方法，`doInSharding()`和`doBetweenSharding()`，因为暂时不用IN和BETWEEN方法，所以就没有写，直接返回null。

__数据表分片策略__

数据表的分片策略是根据股票和时间共同决定的，在sharding-jdbc中是多键分片。根据官方文档，实现`MultipleKeysTableShardingAlgorithm`接口就OK了

```java
import com.dangdang.ddframe.rdb.sharding.api.ShardingValue;
import com.dangdang.ddframe.rdb.sharding.api.strategy.table.MultipleKeysTableShardingAlgorithm;
import org.springframework.stereotype.Component;

import java.text.SimpleDateFormat;
import java.util.Collection;
import java.util.Date;
import java.util.LinkedHashSet;

@Component
public class TableShardingAlgorithm implements MultipleKeysTableShardingAlgorithm {

    /**
     * 根据分片值计算分片结果名称集合.
     *
     * @param availableTargetNames 所有的可用目标名称集合, 一般是数据源或表名称
     * @param shardingValues       分片值集合
     * @return 分片后指向的目标名称集合, 一般是数据源或表名称
     */
    @Override
    public Collection<String> doSharding(Collection<String> availableTargetNames, Collection<ShardingValue<?>> shardingValues) {
        String name = null;
        Date time = null;
        for (ShardingValue<?> shardingValue : shardingValues) {
            if (shardingValue.getColumnName().equals("name")) {
                name = ((ShardingValue<String>) shardingValue).getValue();
            }
            if (shardingValue.getColumnName().equals("time")) {
                time = ((ShardingValue<Date>) shardingValue).getValue();
            }
            if (name != null && time != null) {
                break;
            }
        }
        String timeString = new SimpleDateFormat("yyyy_MM").format(time);
        String suffix = name + "_" + timeString;
        Collection<String> result = new LinkedHashSet<>();
        for (String targetName : availableTargetNames) {
            if (targetName.endsWith(suffix)) {
                result.add(targetName);
            }
        }
        return result;
    }
}
```

__注入分片策略__

以上只是定义了分片算法，还没有形成策略，还没有告诉shrding将哪个字段给分片算法：

```java
import com.cosmos.shardingboot.strategy.DatabaseShardingAlgorithm;
import com.cosmos.shardingboot.strategy.TableShardingAlgorithm;
import com.dangdang.ddframe.rdb.sharding.api.strategy.database.DatabaseShardingStrategy;
import com.dangdang.ddframe.rdb.sharding.api.strategy.table.TableShardingStrategy;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.Collection;
import java.util.LinkedList;

@Configuration
public class ShardingStrategyConfig {

    @Bean
    public DatabaseShardingStrategy databaseShardingStrategy(DatabaseShardingAlgorithm databaseShardingAlgorithm) {
        return new DatabaseShardingStrategy("exchange", databaseShardingAlgorithm);
    }

    @Bean
    public TableShardingStrategy tableShardingStrategy(TableShardingAlgorithm tableShardingAlgorithm) {
        Collection<String> columns = new LinkedList<>();
        columns.add("name");
        columns.add("time");
        return new TableShardingStrategy(columns, tableShardingAlgorithm);
    }

}
```

这样才能形成完成的分片策略。

#### MyBais配置

__Bean__

```java
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Date;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Order {
    /**
     * The Id.
     */
    private long id;
    /**
     * The Name.
     */
    private String name;
    /**
     * The Exchange.
     */
    private String exchange;
    /**
     * The Ask.
     */
    private int ask;
    /**
     * The Bid.
     */
    private int bid;
    /**
     * The Time.
     */
    private Date time;
}
```

__Mapper__

很简单，只实现两个方法

```java
import java.util.List;

public interface OrderMapper {
    int insert(Order order);

    List<Order> list();
}
```

__XML__

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.cosmos.shardingboot.mapper.OrderMapper">
    <insert id="insert" parameterType="com.cosmos.shardingboot.entity.Order">
        INSERT INTO orders (id, `name`, exchange, ask, bid, `time`)
        VALUES (#{id}, #{name}, #{exchange}, #{ask}, #{bid}, #{time})
    </insert>

    <select id="list" resultType="com.cosmos.shardingboot.entity.Order">
        SELECT id, `name`, exchange, ask, bid, `time`
         FROM orders
    </select>

</mapper>
```

__SessionFactory配置__

还要设置一下tick的SessionFactory：

```java
import com.dangdang.ddframe.rdb.sharding.id.generator.self.CommonSelfIdGenerator;
import com.dangdang.ddframe.rdb.sharding.id.generator.self.time.AbstractClock;
import lombok.extern.slf4j.Slf4j;
import org.apache.ibatis.session.SqlSessionFactory;
import org.mybatis.spring.SqlSessionFactoryBean;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.core.io.support.ResourcePatternResolver;

import javax.sql.DataSource;

@Configuration
@Slf4j
@MapperScan("com.cosmos.shardingboot.mapper")
public class MyBatisConfig {

    @Bean
    public SqlSessionFactory sessionFactory(DataSource dataSource) throws Exception {
        final SqlSessionFactoryBean sessionFactory = new SqlSessionFactoryBean();
        sessionFactory.setDataSource(dataSource);

        ResourcePatternResolver resolver = new PathMatchingResourcePatternResolver();
        try {
            sessionFactory.setMapperLocations(resolver.getResources("classpath:mybatis/*.xml"));
            return sessionFactory.getObject();
        } catch (Exception e) {
            log.error("init SqlSessionFactory failed", e);
            throw new RuntimeException(e);
        }
    }

    @Bean
    public CommonSelfIdGenerator commonSelfIdGenerator() {
        CommonSelfIdGenerator.setClock(AbstractClock.systemClock());
        return new CommonSelfIdGenerator();
    }
}
```
这里添加了一个`CommonSelfIdGenerator`，sharding自带的id生成器，看了下代码和`Facebook`的`snowflake`类似。注意：不能把数据库的主键设置成自增的，否则数据双向同步会死的很惨的。

### 测试用例

测试用例只用了INSERT和SELECT

```java
@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest
@Slf4j
public class SpringBootShardingJdbcDemoApplicationTests {

    @Autowired
    private OrderDao orderDao;

    @Autowired
    private CommonSelfIdGenerator commonSelfIdGenerator;

    @Test
    public void insert() {
        Order order1 = new Order(commonSelfIdGenerator.generateId().longValue(), "a", "sh", 100, 200, new Date());
        Order order2 = new Order(commonSelfIdGenerator.generateId().longValue(), "b", "sz", 20, 100, new Date());
        this.orderDao.insert(order1);
        this.orderDao.insert(order2);
    }

    @Test
    public void query() {
        List<Order> orders = orderDao.list();
        for(Order order : orders) {
            log.info("order: {}", order);
        }
    }
}
```

__logback__

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>

    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
            <Pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{35} - %X{fddTraceId} %msg%n</Pattern>
        </encoder>
    </appender>

    <appender name="APPLOG" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <FileNamePattern>${LOGS_DIR:-logs}/server.%d{yyyy-MM-dd}.log</FileNamePattern>
            <MaxHistory>3</MaxHistory>
        </rollingPolicy>
        <layout class="ch.qos.logback.classic.PatternLayout">
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{35} - %X{fddTraceId} %msg%n</pattern>
        </layout>
    </appender>

    <appender name="ERRLOG" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <FileNamePattern>${LOGS_DIR:-logs}/error.%d{yyyy-MM-dd}.log</FileNamePattern>
            <MaxHistory>3</MaxHistory>
        </rollingPolicy>
        <layout class="ch.qos.logback.classic.PatternLayout">
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{35} - %X{fddTraceId} %msg%n</pattern>
        </layout>
        <filter class="ch.qos.logback.classic.filter.LevelFilter">
            <level>ERROR</level>
            <onMatch>ACCEPT</onMatch>
            <onMismatch>DENY</onMismatch>
        </filter>
    </appender>

    <logger name="com.cosmos" additivity="true" level="INFO"/>
    <logger name="com.dangdang" level="DEBUG"/>

    <root>
        <level value="INFO" />
        <appender-ref ref="STDOUT" />
        <appender-ref ref="APPLOG" />
        <appender-ref ref="ERRLOG" />
    </root>

</configuration>
```

日志如下：

插入日志

```console
2017-04-21 11:58:55.271 [main] DEBUG c.d.d.r.s.i.g.s.CommonSelfIdGenerator -  2017-04-21 11:58:55.270-0-0
2017-04-21 11:58:55.273 [main] DEBUG c.d.d.r.s.i.g.s.CommonSelfIdGenerator -  2017-04-21 11:58:55.273-0-0
2017-04-21 11:58:55.359 [main] DEBUG c.d.d.r.s.parser.SQLParserFactory -  Logic SQL: INSERT INTO orders (id, `name`, exchange, ask, bid, `time`)
        VALUES (?, ?, ?, ?, ?, ?), [62149247453102080, a, sh, 100, 200, 2017-04-21 11:58:55.273]
2017-04-21 11:58:55.624 [main] DEBUG c.d.d.r.s.parser.SQLParseEngine -  Parsed SQL result: SQLParsedResult(routeContext=RouteContext(tables=[Table(name=orders, alias=Optional.absent())], sqlStatementType=null, sqlBuilder=null), generatedKeyContext=GeneratedKeyContext(columns=[], columnNameToIndexMap={}, valueTable={}, rowIndex=0, columnIndex=0, autoGeneratedKeys=0, columnIndexes=null, columnNames=null), conditionContexts=[ConditionContext(conditions={Condition.Column(columnName=name, tableName=orders)=Condition(column=Condition.Column(columnName=name, tableName=orders), operator==, values=[a], valueIndices=[1]), Condition.Column(columnName=exchange, tableName=orders)=Condition(column=Condition.Column(columnName=exchange, tableName=orders), operator==, values=[sh], valueIndices=[2]), Condition.Column(columnName=time, tableName=orders)=Condition(column=Condition.Column(columnName=time, tableName=orders), operator==, values=[2017-04-21 11:58:55.273], valueIndices=[5])})], mergeContext=MergeContext(orderByColumns=[], groupByColumns=[], aggregationColumns=[], limit=null))
2017-04-21 11:58:55.634 [main] DEBUG c.d.d.r.s.parser.SQLParseEngine -  Parsed SQL: INSERT INTO [Token(orders)] (id, `name`, exchange, ask, bid , `time`) VALUES (?, ?, ?, ?, ? , ?)
2017-04-21 11:58:55.647 [main] DEBUG c.d.d.r.s.r.s.SingleTableRouter -  Before database sharding orders routes db names: [db_sh, db_sz] sharding columns: [exchange] sharding values: [ShardingValue(logicTableName=orders, columnName=exchange, value=sh, values=[], valueRange=null)]
2017-04-21 11:58:55.650 [main] DEBUG c.d.d.r.s.r.s.SingleTableRouter -  After database sharding orders result: [db_sh]
2017-04-21 11:58:55.650 [main] DEBUG c.d.d.r.s.r.s.SingleTableRouter -  Before table sharding orders routes db names: [DataNode(dataSourceName=db_sh, tableName=orders_a_2017_04), DataNode(dataSourceName=db_sh, tableName=orders_a_2017_05), DataNode(dataSourceName=db_sh, tableName=orders_b_2017_04), DataNode(dataSourceName=db_sh, tableName=orders_b_2017_05), DataNode(dataSourceName=db_sz, tableName=orders_a_2017_04), DataNode(dataSourceName=db_sz, tableName=orders_a_2017_05), DataNode(dataSourceName=db_sz, tableName=orders_b_2017_04), DataNode(dataSourceName=db_sz, tableName=orders_a_2017_05)] sharding columns: [name, time] sharding values: [ShardingValue(logicTableName=orders, columnName=name, value=a, values=[], valueRange=null), ShardingValue(logicTableName=orders, columnName=time, value=2017-04-21 11:58:55.273, values=[], valueRange=null)]
2017-04-21 11:58:55.652 [main] DEBUG c.d.d.r.s.r.s.SingleTableRouter -  After table sharding orders result: [orders_a_2017_04]
2017-04-21 11:58:55.657 [main] DEBUG c.d.d.r.s.router.SQLRouteEngine -  final route result is 1 target
2017-04-21 11:58:55.657 [main] DEBUG c.d.d.r.s.router.SQLRouteEngine -  db_sh:INSERT INTO orders_a_2017_04 (id, `name`, exchange, ask, bid , `time`) VALUES (?, ?, ?, ?, ? , ?) [62149247453102080, a, sh, 100, 200, 2017-04-21 11:58:55.273]
2017-04-21 11:58:55.658 [main] DEBUG c.d.d.r.s.router.SQLRouteEngine -  merge context:MergeContext(orderByColumns=[], groupByColumns=[], aggregationColumns=[], limit=null)
```

查询日志

```console
2017-04-21 11:58:55.853 [main] DEBUG c.d.d.r.s.parser.SQLParserFactory -  Logic SQL: SELECT id, `name`, exchange, ask, bid, `time`
         FROM orders, []
2017-04-21 11:58:55.872 [main] DEBUG c.d.d.r.s.parser.SQLParseEngine -  Parsed SQL result: SQLParsedResult(routeContext=RouteContext(tables=[Table(name=orders, alias=Optional.absent())], sqlStatementType=null, sqlBuilder=null), generatedKeyContext=GeneratedKeyContext(columns=[], columnNameToIndexMap={}, valueTable={}, rowIndex=0, columnIndex=0, autoGeneratedKeys=0, columnIndexes=null, columnNames=null), conditionContexts=[ConditionContext(conditions={})], mergeContext=MergeContext(orderByColumns=[], groupByColumns=[], aggregationColumns=[], limit=null))
2017-04-21 11:58:55.873 [main] DEBUG c.d.d.r.s.parser.SQLParseEngine -  Parsed SQL: SELECT id, `name`, exchange, ask, bid , `time` FROM [Token(orders)]
2017-04-21 11:58:55.873 [main] DEBUG c.d.d.r.s.r.s.SingleTableRouter -  Before database sharding orders routes db names: [db_sh, db_sz] sharding columns: [exchange] sharding values: []
2017-04-21 11:58:55.873 [main] DEBUG c.d.d.r.s.r.s.SingleTableRouter -  After database sharding orders result: [db_sz, db_sh]
2017-04-21 11:58:55.874 [main] DEBUG c.d.d.r.s.r.s.SingleTableRouter -  Before table sharding orders routes db names: [DataNode(dataSourceName=db_sh, tableName=orders_a_2017_04), DataNode(dataSourceName=db_sh, tableName=orders_a_2017_05), DataNode(dataSourceName=db_sh, tableName=orders_b_2017_04), DataNode(dataSourceName=db_sh, tableName=orders_b_2017_05), DataNode(dataSourceName=db_sz, tableName=orders_a_2017_04), DataNode(dataSourceName=db_sz, tableName=orders_a_2017_05), DataNode(dataSourceName=db_sz, tableName=orders_b_2017_04), DataNode(dataSourceName=db_sz, tableName=orders_a_2017_05)] sharding columns: [name, time] sharding values: []
2017-04-21 11:58:55.874 [main] DEBUG c.d.d.r.s.r.s.SingleTableRouter -  After table sharding orders result: [orders_a_2017_05, orders_b_2017_05, orders_b_2017_04, orders_a_2017_04]
2017-04-21 11:58:55.875 [main] DEBUG c.d.d.r.s.router.SQLRouteEngine -  final route result is 7 target
2017-04-21 11:58:55.875 [main] DEBUG c.d.d.r.s.router.SQLRouteEngine -  db_sh:SELECT id, `name`, exchange, ask, bid , `time` FROM orders_b_2017_04 []
2017-04-21 11:58:55.875 [main] DEBUG c.d.d.r.s.router.SQLRouteEngine -  db_sh:SELECT id, `name`, exchange, ask, bid , `time` FROM orders_b_2017_05 []
2017-04-21 11:58:55.875 [main] DEBUG c.d.d.r.s.router.SQLRouteEngine -  db_sh:SELECT id, `name`, exchange, ask, bid , `time` FROM orders_a_2017_04 []
2017-04-21 11:58:55.875 [main] DEBUG c.d.d.r.s.router.SQLRouteEngine -  db_sh:SELECT id, `name`, exchange, ask, bid , `time` FROM orders_a_2017_05 []
2017-04-21 11:58:55.875 [main] DEBUG c.d.d.r.s.router.SQLRouteEngine -  db_sz:SELECT id, `name`, exchange, ask, bid , `time` FROM orders_a_2017_04 []
2017-04-21 11:58:55.876 [main] DEBUG c.d.d.r.s.router.SQLRouteEngine -  db_sz:SELECT id, `name`, exchange, ask, bid , `time` FROM orders_a_2017_05 []
2017-04-21 11:58:55.877 [main] DEBUG c.d.d.r.s.router.SQLRouteEngine -  db_sz:SELECT id, `name`, exchange, ask, bid , `time` FROM orders_b_2017_04 []
2017-04-21 11:58:55.877 [main] DEBUG c.d.d.r.s.router.SQLRouteEngine -  merge context:MergeContext(orderByColumns=[], groupByColumns=[], aggregationColumns=[], limit=null)
2017-04-21 11:58:55.972 [main] DEBUG c.d.d.r.s.m.ShardingResultSets$WrapperResultSet -  651433745 join pipeline
2017-04-21 11:58:55.973 [main] DEBUG c.d.d.r.s.m.ShardingResultSets$WrapperResultSet -  697240075 join pipeline
2017-04-21 11:58:55.976 [main] DEBUG c.d.d.r.s.merger.ResultSetFactory -  Sharding-JDBC: Sharding result sets type is 'MULTIPLE'
2017-04-21 11:58:55.979 [main] DEBUG c.d.d.r.s.m.p.r.IteratorReducerResultSet -  411748515 join pipeline
2017-04-21 11:58:56.001 [main] INFO  c.c.s.SpringBootShardingJdbcDemoApplicationTests -  order: Order(id=61412297490300928, name=a, exchange=sh, ask=100, bid=200, time=Wed Apr 19 11:10:33 CST 2017)
2017-04-21 11:58:56.002 [main] INFO  c.c.s.SpringBootShardingJdbcDemoApplicationTests -  order: Order(id=61417916154773504, name=a, exchange=sh, ask=100, bid=200, time=Wed Apr 19 11:32:52 CST 2017)
2017-04-21 11:58:56.003 [main] INFO  c.c.s.SpringBootShardingJdbcDemoApplicationTests -  order: Order(id=61418033175855104, name=a, exchange=sh, ask=100, bid=200, time=Wed Apr 19 11:33:20 CST 2017)
2017-04-21 11:58:56.003 [main] INFO  c.c.s.SpringBootShardingJdbcDemoApplicationTests -  order: Order(id=61418476123717632, name=a, exchange=sh, ask=100, bid=200, time=Wed Apr 19 11:35:06 CST 2017)
2017-04-21 11:58:56.004 [main] INFO  c.c.s.SpringBootShardingJdbcDemoApplicationTests -  order: Order(id=61418699143249920, name=a, exchange=sh, ask=100, bid=200, time=Wed Apr 19 11:35:59 CST 2017)
2017-04-21 11:58:56.010 [main] INFO  c.c.s.SpringBootShardingJdbcDemoApplicationTests -  order: Order(id=61882120510898176, name=a, exchange=sh, ask=100, bid=200, time=Thu Apr 20 18:17:27 CST 2017)
2017-04-21 11:58:56.010 [main] INFO  c.c.s.SpringBootShardingJdbcDemoApplicationTests -  order: Order(id=62149247453102080, name=a, exchange=sh, ask=100, bid=200, time=Fri Apr 21 11:58:55 CST 2017)
2017-04-21 11:58:56.010 [main] INFO  c.c.s.SpringBootShardingJdbcDemoApplicationTests -  order: Order(id=61418033180049408, name=b, exchange=sz, ask=20, bid=100, time=Wed Apr 19 11:33:20 CST 2017)
2017-04-21 11:58:56.010 [main] INFO  c.c.s.SpringBootShardingJdbcDemoApplicationTests -  order: Order(id=61418476127911936, name=b, exchange=sz, ask=20, bid=100, time=Wed Apr 19 11:35:06 CST 2017)
2017-04-21 11:58:56.010 [main] INFO  c.c.s.SpringBootShardingJdbcDemoApplicationTests -  order: Order(id=61418699147444224, name=b, exchange=sz, ask=20, bid=100, time=Wed Apr 19 11:35:59 CST 2017)
2017-04-21 11:58:56.011 [main] INFO  c.c.s.SpringBootShardingJdbcDemoApplicationTests -  order: Order(id=61882120515092480, name=b, exchange=sz, ask=20, bid=100, time=Thu Apr 20 18:17:27 CST 2017)
2017-04-21 11:58:56.011 [main] INFO  c.c.s.SpringBootShardingJdbcDemoApplicationTests -  order: Order(id=62149247465684992, name=b, exchange=sz, ask=20, bid=100, time=Fri Apr 21 11:58:55 CST 2017)
```

可见sharding-jdbc底层针对DML和DQL操作不同：

* 对DML，其实是对SQL做解析，然后拆分成针对具体sharding的DML进行操作；
* 对DQL，解析后对具体分片做操作，然后再Merge返回；

至此实现增量分库分表。
