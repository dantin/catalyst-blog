---
title: 一致性哈希
date: 2016-09-02 16:17:46
categories: 学术
tags: Distributed
toc: true
---

本文介绍一致性哈希算法（Consistent Hashing）及其在分布式系统中的应用。首先本文会描述一个在日常开发中经常会遇到的问题场景，借此介绍一致性哈希算法以及这个算法如何解决此问题；接下来会对这个算法进行相对详细的描述，并讨论一些如虚拟节点等与此算法应用相关的话题。

### 分布式缓存问题

假设我们有一个网站，最近发现随着流量增加，服务器压力越来越大，之前直接读写数据库的方式不太给力了，于是我们想引入Memcached作为缓存机制。现在我们一共有三台机器可以作为Memcached服务器，如下图所示。

![分布式缓存的问题](/images/consistent-hashing-problem.png "Consistent Hashing Problem")

很显然，最简单的策略是将每一次Memcached请求随机发送到一台Memcached服务器，但是这种策略可能会带来两个问题：一是同一份数据可能被存在不同的机器上而造成数据冗余，二是有可能某数据已经被缓存但是访问却没有命中，因为无法保证对相同key的所有访问都被发送到相同的服务器。因此，随机策略无论是时间效率还是空间效率都非常不好。

要解决上述问题只需做到如下一点：保证对相同key的访问会被发送到相同的服务器。很多方法可以实现这一点，最常用的方法是计算哈希。例如对于每次访问，可以按如下算法计算其哈希值：

```bash
h = Hash(key) % 3
```

其中Hash是一个从字符串到正整数的哈希映射函数。这样，如果我们将Memcached Server分别编号为0、1、2，那么就可以根据上式和key计算出服务器编号h，然后去访问。

这个方法虽然解决了上面提到的两个问题，但是存在一些其它的问题。如果将上述方法抽象，可以认为通过：

```bash
h = Hash(key) % N
```

这个算式计算每个key的请求应该被发送到哪台服务器，其中N为服务器的台数，并且服务器按照0 – (N-1)编号。

这个算法的问题在于容错性和扩展性不好。所谓容错性是指当系统中某一个或几个服务器变得不可用时，整个系统是否可以正确高效运行；而扩展性是指当加入新的服务器后，整个系统是否可以正确高效运行。

现假设有一台服务器宕机了，那么为了填补空缺，要将宕机的服务器从编号列表中移除，后面的服务器按顺序前移一位并将其编号值减一，此时每个key就要按h = Hash(key) % (N-1)重新计算；同样，如果新增了一台服务器，虽然原有服务器编号不用改变，但是要按h = Hash(key) % (N+1)重新计算哈希值。因此系统中一旦有服务器变更，大量的key会被重定位到不同的服务器从而造成大量的缓存不命中。而这种情况在分布式系统中是非常糟糕的。

一个设计良好的分布式哈希方案应该具有良好的单调性，即服务节点的增减不会造成大量哈希重定位。一致性哈希算法就是这样一种哈希方案。

### 一致性哈希算法

#### 算法简述

一致性哈希算法（Consistent Hashing）最早在论文[《Consistent Hashing and Random Trees: Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web》](http://www.akamai.com/dl/technical_publications/ConsistenHashingandRandomTreesDistributedCachingprotocolsforrelievingHotSpotsontheworldwideweb.pdf)中被提出。简单来说，一致性哈希将整个哈希值空间组织成一个虚拟的圆环，如假设某哈希函数H的值空间为0 - 2^32-1（即哈希值是一个32位无符号整形），整个哈希空间环如下：

![哈希空间环](/images/consistent-hashing-01.png "Hashing Space Ring")

整个空间按顺时针方向组织。0和2^32-1在零点中方向重合。

下一步将各个服务器使用H进行一个哈希，具体可以选择服务器的ip或主机名作为关键字进行哈希，这样每台机器就能确定其在哈希环上的位置，这里假设将上文中三台服务器使用ip地址哈希后在环空间的位置如下：

![哈希空间基准位置](/images/consistent-hashing-02.png "Hashing Space Base")

接下来使用如下算法定位数据访问到相应服务器：将数据key使用相同的函数H计算出哈希值h，通根据h确定此数据在环上的位置，从此位置沿环顺时针“行走”，第一台遇到的服务器就是其应该定位到的服务器。

例如我们有A、B、C、D四个数据对象，经过哈希计算后，在环空间上的位置如下：

![哈希空间数据位置](/images/consistent-hashing-03.png "Hashing Space Data")

根据一致性哈希算法，数据A会被定为到Server 1上，D被定为到Server 3上，而B、C分别被定为到Server 2上。

#### 容错性与可扩展性分析

下面分析一致性哈希算法的容错性和可扩展性。现假设Server 3宕机了：

![哈希空间容错](/images/consistent-hashing-04.png "Hashing Space Broken")

可以看到此时A、C、B不会受到影响，只有D节点被重定位到Server 2。一般的，在一致性哈希算法中，如果一台服务器不可用，则受影响的数据仅仅是此服务器到其环空间中前一台服务器（即顺着逆时针方向行走遇到的第一台服务器）之间数据，其它不会受到影响。

下面考虑另外一种情况，如果我们在系统中增加一台服务器Memcached Server 4：

![哈希空间增加机器](/images/consistent-hashing-05.png "Hashing Space New")

此时A、D、C不受影响，只有B需要重定位到新的Server 4。一般的，在一致性哈希算法中，如果增加一台服务器，则受影响的数据仅仅是新服务器到其环空间中前一台服务器（即顺着逆时针方向行走遇到的第一台服务器）之间数据，其它不会受到影响。

综上所述，一致性哈希算法对于节点的增减都只需重定位环空间中的一小部分数据，具有较好的容错性和可扩展性。

#### 虚拟节点

一致性哈希算法在服务节点太少时，容易因为节点分部不均匀而造成数据倾斜问题。例如我们的系统中有两台服务器，其环分布如下：

![虚拟节点1](/images/consistent-hashing-06.png "Virtual Node 1")

此时必然造成大量数据集中到Server 1上，而只有极少量会定位到Server 2上。为了解决这种数据倾斜问题，一致性哈希算法引入了虚拟节点机制，即对每一个服务节点计算多个哈希，每个计算结果位置都放置一个此服务节点，称为虚拟节点。具体做法可以在服务器ip或主机名的后面增加编号来实现。例如上面的情况，我们决定为每台服务器计算三个虚拟节点，于是可以分别计算“Memcached Server 1#1”、“Memcached Server 1#2”、“Memcached Server 1#3”、“Memcached Server 2#1”、“Memcached Server 2#2”、“Memcached Server 2#3”的哈希值，于是形成六个虚拟节点：

![虚拟节点2](/images/consistent-hashing-07.png "Virtual Node 2")

同时数据定位算法不变，只是多了一步虚拟节点到实际节点的映射，例如定位到“Memcached Server 1#1”、“Memcached Server 1#2”、“Memcached Server 1#3”三个虚拟节点的数据均定位到Server 1上。这样就解决了服务节点少时数据倾斜的问题。在实际应用中，通常将虚拟节点数设置为32甚至更大，因此即使很少的服务节点也能做到相对均匀的数据分布。

### 实现

参考[groupcache consistent hash算法源码](https://github.com/golang/groupcache/blob/master/consistenthash/consistenthash.go)

#### 数据结构

Map结构，定义核心数据结构,其中hash是哈希函数，用于对key进行hash，keys字段保存所有的节点（包括虚拟节点）是可排序的，hashmap则是虚拟节点到真实节点的映射。

```go
type Map struct {
    hash     Hash // hash 函数
    replicas int
    keys     []int // Sorted
    hashMap  map[int]string
}
```

一致性哈希算法在服务节点太少时，容易因为节点分部不均匀而造成数据倾斜问题。一致性哈希算法引入了虚拟节点机制，即对每一个服务节点计算多个哈希，每个计算结果位置都放置一个此服务节点，称为虚拟节点。replicas是指的是每个节点和虚拟节点的个数。

#### 增加

Map的Add方法，添加节点到圆环，参数是一个或者多个string，对每一个key关键字进行哈希，这样每台机器就能确定其在哈希环上的位置，在添加每个关键字的时候，并添加对应的虚拟节点，每个真实节点和虚拟节点个数有replicas字段指定，保存虚拟节点到真实节点的对应关系到hashmap字段。

```go
// Adds some keys to the hash.
func (m *Map) Add(keys ...string) {
    for _, key := range keys {
        for i := 0; i < m.replicas; i++ {
            hash := int(m.hash([]byte(strconv.Itoa(i) + key)))
            m.keys = append(m.keys, hash)
            m.hashMap[hash] = key
        }
    }
    sort.Ints(m.keys)
}
```
比如在测试用例中， hash.Add("6", "4", "2")，则所有的节点是 2, 4, 6, 12, 14, 16, 22, 24, 26, 当has.Get('11') 时，对应的节点是12，而12对应的真实节点是2

hash.Add("6", "4", "2")是数据值：

```bash
2014/02/20 15:45:16 replicas: 3
2014/02/20 15:45:16 keys: [2 4 6 12 14 16 22 24 26]
2014/02/20 15:45:16 hashmap map[16:6 26:6 4:4 24:4 2:2 6:6 14:4 12:2 22:2]
```

#### 获取

Get方法根据提供的key定位数据访问到相应服务器节点，算法是：将数据key使用相同的哈希函数H计算出哈希值h，通根据h确定此数据在环上的位置，从此位置沿环顺时针“行走”，第一台遇到的服务器就是其应该定位到的服务器。

```go
// Gets the closest item in the hash to the provided key.
func (m *Map) Get(key string) string {
    if m.IsEmpty() {
        return ""
    }

    hash := int(m.hash([]byte(key)))

    // 顺时针“行走”，找到第一个大于哈希值的节点
    for _, v := range m.keys {
        if v >= hash {
            return m.hashMap[v] // 返回真实节点
        }
    }

    // hash值大于最大节点哈希值的情况
    return m.hashMap[m.keys[0]]
}
```

### 总结

目前一致性哈希基本成为了分布式系统组件的标准配置，例如Memcached的各种客户端都提供内置的一致性哈希支持。本文只是简要介绍了这个算法，更深入的内容可以参看论文[《Consistent Hashing and Random Trees: Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web》](http://www.akamai.com/dl/technical_publications/ConsistenHashingandRandomTreesDistributedCachingprotocolsforrelievingHotSpotsontheworldwideweb.pdf)，同时提供一个[C语言版本的实现](http://www.codeproject.com/KB/recipes/lib-conhash.aspx)供参考。

参考

[CodingLabs](http://blog.codinglabs.org/articles/consistent-hashing.html)
[segmentfault](https://segmentfault.com/a/1190000000414004)
[July的算法总结](http://the-art-of-programming-by-july.readthedocs.io/en/latest/ebook/zh/%E4%B8%80%E8%87%B4%E6%80%A7%E5%93%88%E5%B8%8C%E7%AE%97%E6%B3%95/)
