+++
date = "2017-04-18T15:06:26+08:00"
title = "SpringBoot和MyBatis的整合办法"
categories = ["Engineering"]
tags = ["SpringBoot", "MyBatis"]
description = "本文记录SpringBoot和MyBatis的整合办法"
slug = "springboot-mybatis-integration"
+++

SpringBoot集成了SpringJDBC与JPA，但是没有集成MyBatis，所以，想要使用MyBatis就要自己去集成。本文记录简单的集成方法。

### POM

引入必须的包，说明：

* spring-boot-starter-jdbc：引入与数据库操作相关的依赖，例如：`daoSupport`等
* druid：阿里巴巴的数据源
* mysql-connector-java：MySQL连接jar，`scope`为`runtime`
* mybatis和mybatis-spring：MyBatis相关jar

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

### application.yml

项目配置文件，这里主要注明数据库连接、用户名、密码等连接信息

```console
server:
  port: 9120

jdbc:
  driver-class-name: com.mysql.jdbc.Driver
  url: jdbc:mysql://127.0.0.1:3306/db_sh?useUnicode=true&autoReconnect=true&rewriteBatchedStatements=true
  username: root
  password:
```

### 配置

数据源配置`DataSourceConfig.java`

```java
@Configuration
@Slf4j
public class DataSourceConfig {

    private final Environment env;

    @Autowired
    public DataSourceConfig(Environment env) {
        this.env = env;
    }

    @Bean
    @Primary
    public DataSource dataSource() {
        DruidDataSource druidDataSource = new DruidDataSource();
        druidDataSource.setDriverClassName(env.getProperty("jdbc.driverClassName"));
        druidDataSource.setUrl(env.getProperty("jdbc.url"));
        druidDataSource.setUsername(env.getProperty("jdbc.username"));
        druidDataSource.setPassword(env.getProperty("jdbc.password"));
        return druidDataSource;
    }

}
```

`@Primary`注解表示在同一个接口有多个实现类可以注入的时候，默认选择哪一个，而不是让@autowire注解报错。

MyBatis SqlSessionFactory配置，`MyBatisConfig.java`

```java
@Configuration
@Slf4j
@MapperScan("com.cosmos.shardingboot.mapper")
public class MyBatisConfig {

    @Bean
    public SqlSessionFactory sessionFactory(DataSource dataSource) throws Exception {
        final SqlSessionFactoryBean sessionFactory = new SqlSessionFactoryBean();
        sessionFactory.setDataSource(dataSource);  // 指定数据源(这个必须有，否则报错)
        
        // 下边用于*.xml文件，如果整个持久层操作不需要使用到xml文件的话（只用注解就可以搞定），则不加
        ResourcePatternResolver resolver = new PathMatchingResourcePatternResolver();
        try {
            // 指定xml文件位置
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

`@MapperScan`注解：指定扫描的mapper接口所在的包

### Mapper

说明：该接口中有两个方法，

* 一个普通插入：直接用注解搞定
* 一个插入返回主键：需要使用XML来搞定

```java
public interface OrderMapper {
    int insert(Order order);

    @Insert("INSERT INTO tb_user(username, password) VALUES(#{username},#{password})")
    int insertUser(@Param("username") String username, @Param("password")  String password);
}
```

若不需要自动返回主键，不需要使用XML的外部文件。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.cosmos.shardingboot.mapper.OrderMapper">
    <!-- 若不需要自动返回主键，将useGeneratedKeys="true" keyProperty="id"去掉即可(当然如果不需要自动返回主键，直接用注解即可) -->
    <insert id="insert"
            parameterType="com.cosmos.shardingboot.entity.Order"
            useGeneratedKeys="true" keyProperty="id">
        INSERT INTO `order` (id, `name`, exchange, ask, bid, `time`)
        VALUES (#{id}, #{name}, #{exchange}, #{ask}, #{bid}, #{time})
    </insert>

</mapper>
```

### 测试

进入项目的pom.xml文件所在目录，执行"mvn spring-boot:run"（这是spring-boot推荐的运行方式）。

另外一种在主类上右击-->"run as"-->"java application"，不常用

测试用例如下：

```java
@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest
public class SpringBootShardingJdbcDemoApplicationTests {

    @Autowired
    private OrderDao orderDao;

    @Autowired
    private CommonSelfIdGenerator commonSelfIdGenerator;

    @Test
    public void contextLoads() {
        Order order = new Order(commonSelfIdGenerator.generateId().longValue(), "a", "sh", 100, 200, new Date());
        this.orderDao.insert(tick);
    }
}
```

参考：

[cnblogs.com](http://www.cnblogs.com/java-zhao/p/5350021.html)