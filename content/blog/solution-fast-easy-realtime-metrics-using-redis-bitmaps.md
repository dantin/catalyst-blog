+++
date = "2016-09-29T10:02:48+08:00"
title = "使用Redis bitmaps实现快速、简单、实时统计"
categories = ["Engineering"]
tags = ["Redis", "Solution"]
description = "本文记录利用Redis实现快速、简单、实时的数据统计"
slug = "solution-fast-easy-realtime-metrics-using-redis-bitmaps"
+++

[Spool](http://www.getspool.com/)的重要统计数据是实时计算的。Redis的bitmap让我们可以实时的进行类似的统计，并且极其节省空间。在模拟1亿2千8百万用户的模拟环境下，在一台MacBookPro上，典型的统计如“日用户数”(dailyunique users) 的时间消耗小于50ms, 占用16MB内存。Spool现在还没有1亿2千8百万用户，但是我们的方案可以应对这样的规模。我们想分享这是如何做到的，也许能帮到其它创业公司。

### Redis Bitmaps快速入门

#### Bitmap(即Bitset)

Bitmap是一串连续的2进制数字（0或1），每一位所在的位置为偏移(offset)，在bitmap上可执行AND,OR,XOR以及其它位操作。

#### 位图计数

位图计数统计的是bitmap中值为1的位的个数。位图计数的效率很高，例如，一个bitmap包含10亿个位，90%的位都置为1，在一台MacBook Pro上对其做位图计数需要21.1ms。SSE4甚至有对整形(integer)做位图计数的硬件指令。

![Bitmap Population Count](/images/redis_bitmap_population_count.png "Bitmap Population Count")

#### Redis Bitmaps

Redis允许使用二进制数据的Key(binary keys) 和二进制数据的Value(binary values)。Bitmap就是二进制数据的value。Redis的 setbit(key, offset, value)操作对指定的key的value的指定偏移(offset)的位置1或0，时间复杂度是O(1)。

### 一个简单的例子：日活跃用户

为了统计今日登录的用户数，我们建立了一个bitmap,每一位标识一个用户ID。当某个用户访问我们的网页或执行了某个操作，就在bitmap中把标识此用户的位置为1。在Redis中获取此bitmap的key值是通过用户执行操作的类型和时间戳获得的。

![Unique Users](/images/redis_bitmap_unique_users.png "Unique Users")

这个简单的例子中，每次用户登录时会执行一次redis.setbit(daily_active_users, user_id, 1)，将bitmap中对应位置的位置为1，时间复杂度是O(1)。统计bitmap结果显示有今天有9个用户登录。Bitmap的key是daily_active_users，它的值是1011110100100101。

因为日活跃用户每天都变化，所以需要每天创建一个新的bitmap。我们简单地把日期添加到key后面，实现了这个功能。例如，要统计某一天有多少个用户至少听了一个音乐app中的一首歌曲，可以把这个bitmap的redis key设计为play:yyyy-mm-dd-hh。当用户听了一首歌曲，我们只是简单地在bitmap中把标识这个用户的位置为1，时间复杂度是O(1)。

```console
redis.setbit(play:yyyy-mm-dd, user_id, 1)
```

今天听过歌曲的用户就是key是play:yyyy-mm-dd的bitmap的位图计数。如果要按周或月统计，只要对这周或这个月的所有bitmap求并集，得出新的bitmap，在对它做位图计数。

![Union](/images/redis_bitmap_union.png "Union")

利用这些bitmap做其它复杂的统计也非常容易。例如，统计11月听过歌曲的高级用户(premium user)：

```console
(play:2011-11-01∪ play:2011-11-02∪ … ∪ play:2011-11-30)∩premium:2011-11
```

#### 1亿2千8百万用户的性能比较

下面的表格显示了在1亿2千8百万用户上完成的时间粒度为1天，一周，一个月的用户统计的时间消耗比较

| PERIOD  | TIME (MS) |
| ------- | --------- |
| Daily   | 50.2      |
| Weekly  | 392.0     |
| Monthly | 1624.8    |

### 优化

前面的例子中，我们把日统计，周统计，月统计缓存到Redis，以加快统计速度。

这是一种非常灵活的方法。这样进行缓存的额外红利是可以进行更多的统计，如每周活跃的手机用户—求手机用户的bitmap与周活跃用户的交集。或者，如果要统计过去n天的活跃用户数，缓存的日活跃用户使这样的统计变得简单——从cache中获取过去n-1天的日活跃用户bitmap和今天的bitmap,对它们做并集(Union)，时间消耗是50ms。

### 示例代码

下面的Java代码用来统计某个用户操作在某天的活跃用户。

```java
import redis.clients.jedis.Jedis;
import java.util.BitSet;
...
  Jedis redis = new Jedis("localhost");
...
  public int uniqueCount(String action, String date) {
    String key = action + ":" + date;
    BitSet users = BitSet.valueOf(redis.get(key.getBytes()));
    return users.cardinality();
  }
```

下面的Java代码用来统计某个用户操作在一个指定多个日期的活跃用户。

```java
import redis.clients.jedis.Jedis;
import java.util.BitSet;
...
  Jedis redis = new Jedis("localhost");
...
  public int uniqueCount(String action, String... dates) {
    BitSet all = new BitSet();
    for (String date : dates) {
      String key = action + ":" + date;
      BitSet users = BitSet.valueOf(redis.get(key.getBytes()));
      all.or(users);
    }
    return all.cardinality();
  }
```

参考

[getspool blog](http://blog.getspool.com/2011/11/29/fast-easy-realtime-metrics-using-redis-bitmaps/)
