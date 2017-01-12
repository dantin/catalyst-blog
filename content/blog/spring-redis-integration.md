+++
date = "2016-04-14T20:33:56+08:00"
title = "使用Jedis整合Spring和Redis"
categories = ["Engineering"]
tags = ["Spring", "Redis"]
description = "本文记录Spring和Redis的整合过程，适用于需要通过Spring连接Redis，但又不想使用Spring-data-redis的人"
slug = "spring-redis-integration"
+++

本文记录Spring和Redis的整合过程，适用于需要通过Spring连接Redis，但又不想使用Spring-data-redis的人。

### 配置连接池

这里使用Jedis的ShardedJedisPool来管理，我们定义该配置文件为：applicationContext-redis.xml，全部内容如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="
          http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-4.2.xsd">

    <description>Redis相关配置</description>

    <!--context:property-placeholder location="classpath:conf/properties/redis.properties" ignore-unresolvable="true" /-->
    
    <!-- jedis pool config配置 -->
    <bean id="jedisPoolConfig" class="redis.clients.jedis.JedisPoolConfig">
        <property name="maxTotal" value="20"/>
        <property name="maxIdle" value="5"/>
        <property name="minIdle" value="1"/>
        <property name="maxWaitMillis" value="3000"/>
        <property name="testOnBorrow" value="true"/>
        <property name="testOnReturn" value="true"/>
    </bean>

    <!-- Sharded Jedis Pool -->
    <bean id="shardedJedisPool" class="redis.clients.jedis.ShardedJedisPool">
        <constructor-arg index="0" ref="jedisPoolConfig" />
        <constructor-arg index="1">
            <list>
                <bean class="redis.clients.jedis.JedisShardInfo">
                    <constructor-arg name="host" value="redis://127.0.0.1:6379/0" />
                </bean>
            </list>
        </constructor-arg>
    </bean>

    <!-- Jedis Data Source -->
    <bean id="jedisDataSource" class="com.cosmos.data.redis.core.JedisDataSource">
        <constructor-arg index="0" ref="shardedJedisPool"/>
    </bean>

    <bean id="jedisTemplate" class="com.cosmos.data.redis.core.JedisTemplate"/>

</beans>
```

注意：

1. 如果你有多个数据源需要通过`<context:property-placeholder>`管理，且不愿意放在一个配置文件里，那么一定要加上`ignore-unresolvable=“true"`
2. 注意新版的（具体从哪个版本开始不清楚，有兴趣可以查一下）JedisPoolConfig的property name，不再是maxActive而是maxTotal，而且没有maxWait属性，建议看一下Jedis源码。
3. ShardedJedisPool有多种构造函数，选择你需要的（具体看源码），示例中只初始化了一个分片，并使用了通过指定host的构造器（具体格式见下文），如果有集群，在`<list>`下增加新的`<bean>`即可。
4. 当然，你的spring核心配置文件中得有`<context:component-scan base-package="com.xxxx.xxx"/>`扫描组件。

另：redis.uri的格式

```bash
redis://[密码]@[服务器地址]:[端口]/[db index]
```

### 代码实现

用统一的类来管理Jedis实例的生成和回收

```java
package com.cosmos.data.redis.core;

import com.cosmos.data.redis.RedisException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import redis.clients.jedis.ShardedJedis;
import redis.clients.jedis.ShardedJedisPool;

/**
 * Jedis Data Source
 */
public class JedisDataSource {

    private static final Logger logger = LoggerFactory.getLogger(JedisDataSource.class);

    private ShardedJedisPool shardedJedisPool;

    public JedisDataSource(ShardedJedisPool shardedJedisPool) {
        this.shardedJedisPool = shardedJedisPool;
    }

    /**
     * @return Redis客户端对象
     */
    public ShardedJedis getRedisClient() {
        try {
            return shardedJedisPool.getResource();
        } catch (Exception e) {
            logger.error("[{}] getRedisClient error!", JedisDataSource.class.getSimpleName());
            throw new RedisException("getRedisClient error!", e);
        }
    }

    public void returnResource(ShardedJedis shardedJedis) {
        if(shardedJedis != null) {
            shardedJedis.close();
        }
    }

    public void returnResource(ShardedJedis shardedJedis, boolean broken) {
        if(shardedJedis != null) {
            shardedJedis.close();
        }
    }
}
```

这个类控制Jedis实例的生成和回收。

具体的Jedis操作类

```java
package com.cosmos.data.redis.core;

import com.cosmos.data.redis.RedisException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import redis.clients.jedis.ShardedJedis;

import java.util.Map;

/**
 * Jedis Template
 *
 * 与Redis交互的核心类
 */
public class JedisTemplate {

    private static final Logger logger = LoggerFactory.getLogger(JedisTemplate.class);

    @Autowired
    private JedisDataSource redisDataSource;

    /**
     * 有返回结果的回调接口定义。
     */
    private interface JedisAction<T> {
        T action(ShardedJedis shardedJedis);
    }

    /**
     * 无返回结果的回调接口定义。
     */
    private interface JedisActionNoResult {
        void action(ShardedJedis shardedJedis);
    }

    /**
     * 执行有返回结果的action。
     */
    private <T> T execute(JedisAction<T> jedisAction) {
        ShardedJedis shardedJedis = null;
        boolean broken = false;
        try {
            shardedJedis = redisDataSource.getRedisClient();
            return jedisAction.action(shardedJedis);
        } catch (Exception e) {
            logger.error("Redis action failed!", e);
            broken = true;
            throw e;
        } finally {
            redisDataSource.returnResource(shardedJedis, broken);
        }
    }

    /**
     * 执行无返回结果的action。
     */
    private void execute(JedisActionNoResult jedisAction) {
        ShardedJedis shardedJedis = null;
        boolean broken = false;
        try {
            shardedJedis = redisDataSource.getRedisClient();
            jedisAction.action(shardedJedis);
        } catch (Exception e) {
            logger.error("Redis action failed!", e);
            broken = true;
            throw new RedisException("No");
        } finally {
            redisDataSource.returnResource(shardedJedis, broken);
        }
    }

    /**
     * 设置键值
     *
     * @param key   键
     * @param value 值
     * @return 返回状态
     */
    public String set(String key, String value) {
        return execute(shardedJedis -> {
            return shardedJedis.set(key, value);
        });
    }

    /**
     * 获取键值
     *
     * @param key 键
     * @return 值
     */
    public String get(String key) {
        return execute(shardedJedis -> {
            return shardedJedis.get(key);
        });
    }

    /**
     * 自增键值, 若键不存在, 则键值初始化为0
     *
     * @param key 键
     * @return 自增后的值
     */
    public Long incr(String key) {
        return execute(shardedJedis -> {
            return shardedJedis.incr(key);
        });
    }

    /**
     * 判断键是否存在
     *
     * @param key 键
     * @return 是否存在
     */
    public Boolean exists(String key) {
        return execute(shardedJedis -> {
            return shardedJedis.exists(key);
        });
    }

    /**
     * 判断键的类型
     *
     * @param key 键
     * @return 类型
     */
    public String type(String key) {
        return execute(shardedJedis -> {
            return shardedJedis.type(key);
        });
    }

    /**
     * 设置键的失效时间
     *
     * @param key     键
     * @param seconds 失效时间, 单位: 秒
     * @return 是否设置成功
     */
    public Long expire(String key, int seconds) {
        return execute(shardedJedis -> {
            return shardedJedis.expire(key, seconds);
        });
    }

    /**
     * 设置键在某个时间点失效
     *
     * @param key      键
     * @param unixTime 失效时间点
     * @return 是否设置成功
     */
    public Long expireAt(String key, long unixTime) {
        return execute(shardedJedis -> {
            return shardedJedis.expireAt(key, unixTime);
        });
    }

    /**
     * 获取键的失效时间
     *
     * @param key 键
     * @return 失效时间
     */
    public Long ttl(String key) {
        return execute(shardedJedis -> {
            return shardedJedis.ttl(key);
        });
    }

    /**
     * 在键的偏移位设置值
     *
     * @param key    键
     * @param offset 偏移位置
     * @param value  值, 0/1
     * @return 该位置的原值
     */
    public Boolean setbit(String key, long offset, boolean value) {
        return execute(shardedJedis -> {
            return shardedJedis.setbit(key, offset, value);
        });
    }

    /**
     * 获取键所在偏移位的值
     *
     * @param key    键
     * @param offset 偏移位置
     * @return 偏移位的值
     */
    public Boolean getbit(String key, long offset) {
        return execute(shardedJedis -> {
            return shardedJedis.getbit(key, offset);
        });
    }

    /**
     * 在键的偏移位设置新值
     *
     * @param key    键
     * @param offset 偏移位置
     * @param value  值
     * @return 修改后值的长度
     */
    public Long setrange(String key, long offset, String value) {
        return execute(shardedJedis -> {
            return shardedJedis.setrange(key, offset, value);
        });
    }

    /**
     * 获取偏移开始位置至结束位置的值
     *
     * @param key         键
     * @param startOffset 偏移开始位置
     * @param endOffset   偏移结束位置
     * @return 部分值
     */
    public String getrange(String key, long startOffset, long endOffset) {
        return execute(shardedJedis -> {
            return shardedJedis.getrange(key, startOffset, endOffset);
        });
    }

    /**
     * 设置哈希键中的某一个域的值
     *
     * @param key   键
     * @param field 域
     * @param value 值
     * @return 1, 新增 / 0, 更新
     */
    public Long hset(String key, String field, String value) {
        return execute(shardedJedis -> {
            return shardedJedis.hset(key, field, value);
        });
    }

    /**
     * 获取哈希键中的所有域值
     *
     * @param key 键
     * @return 哈希键中的所有域值
     */
    public Map<String, String> hgetall(String key) {
        return execute(shardedJedis -> {
            return shardedJedis.hgetAll(key);
        });
    }
}

```

以上代码全部搞定，接下来在业务代码里加载RedisClientTemplate即可。
