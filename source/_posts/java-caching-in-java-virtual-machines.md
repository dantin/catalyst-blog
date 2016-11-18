---
title: JVM中的DNS缓存
date: 2016-11-17 16:21:09
categories: 工程
tags: [Java, JVM]
toc: true
---

Java有个概念叫DNS Caching in Java Virtual Machines。它不像其他大部分的Stand-alone的桌面应用和网络应用一样，直接将系统的DNS Flush一下或重启就可以生效。Jdk为了提升系统性能，通过InetAddress将网络访问后的DNS解析结果cache起来，并提供了以下方法来查询hostname和IP的匹配关系。

> getAddress(): Returns the raw IP Address for this object. 
> getAllByName(String host): Given the name of host, an array of IP address is returned. 
> getByAddress(byte[] addr): Returns an InetAddress object given the raw IP address 
> getByAddress(String host, byte[] addr): Create an InetAddress based on the provided host name and IP address 
> getByName(String host): Determines the IP address of a host, given the host's name. 
> getCanonicalHostName(): Gets the fully qualified domain name for this IP address. 
> getHostAddress(): Returns the IP address string in textual presentation 
> getHostName(): Gets the host name for this IP address 
> getLocalHost(): Returns the local host.


### 配置属性

除了InetAddress可以查询缓存的信息， Java中用了四个属性来管理JVM DNS Cache TTL（Time To Live），即：DNS Cache的缓存失效时间。

__networkaddress.cache.ttl__

* 缓存正确解析后的IP地址
* 指定的整数表明会缓存正确解析的DNS多长时间
* 默认值为-1， 代表在JVM启动期间会一直缓存
* 如果设置为0，则表示不缓存正确解析的结果
* 如果不设置，默认缓存30秒

__networkaddress.cache.negative.ttl__

* 缓存解析失败结果，可以减少DNS服务器压力
* 指定的整数表明会缓存解析失败结果多长时间
* 默认值为10，表示JVM会cache失败解析结果10秒
* 如果该值设置为0, 则表示不缓存失败结果

__sun.net.inetaddr.ttl__

* 私有变量，对应networkaddress.cache.ttl
* 这个参数，只能在命令行中被设置值。

__sun.net.inetaddr.negative.ttl__

* 私有变量，对应networkaddress.cache.negative.ttl，
* 同样，只能在命令行中被设置值。

### 禁用缓存办法

使用DNS Caching in Java Virtual Machines文中提到的方式，我们可以通过以下三种方式来进行对host修改后的实时生效：

#### 修改java.security

编辑`$JAVA_HOME/jre/lib/secerity/java.security`文件中将网络地址缓存属性（networkaddress.cache.ttl和networkaddress.cache.negative.ttl）的值修改为你想要的值；优点是一劳永逸性的修改，非编程式的解决方案; 但java.security是公用资源文件，这个方式会影响这台机器上所有的JVM。

#### 代码配置

在代码中可直接将动态配置，方式如下： 

```java
java.security.Security.setProperty(“propertyname”, “value”) 

// Example
Security.setProperty("networkaddress.cache.ttl", "0"); 
Security.setProperty("networkaddress.cache. negative .ttl", "0");
```

好处时，只影响当前的JVM，不影响他人，但缺点是，它是编程式的， 但正是利用了这一点，让我们的host文件修改可以实时生效。

#### 启动参数

在JVM启动时，在命令行中加入`-Dsun.net.inetaddr.ttl=value`和`-Dsun.net.inetaddr.negative.ttl=value`这两个指令，也可以起到配置缓存DNS失效时间作用。__注意__：这个方式，只在当`networkaddress.cache.*`属性没有配置时才能起作用。

#### 反射机制

除了上面提到的问题，我还找到一个资料，是通过Java反射机制，将InetAddresss类中的static变量addressCache强行修改方式，来达到实时生效hosts文件修改的目的。这种方式同上面提到的修改Java DNS Cache TTL不同，是不会去修改Cache配置，而是将运行中的缓存的IP/hostname对应关系数据强制修改。经过测试验证，确实可行。

```java
public static void modifyDnsCachePolicy(String hostname) throws Exception { 
        // 开始修改缓存数据 
        Class inetAddressClass = InetAddress.class; 
        final Field cacheField = inetAddressClass.getDeclaredField("addressCache"); 
        cacheField.setAccessible(true); 
        final Object obj = cacheField.get(inetAddressClass); 
        Class cacheClazz = obj.getClass(); 
        final Field cacheMapField = cacheClazz.getDeclaredField("cache"); 
        cacheMapField.setAccessible(true); 
        final Map cacheMap = (Map) cacheMapField.get(obj); 
        cacheMap.remove(hostname); 
        // 修改缓存数据结束 
    }
```

### 实践方式

下面是这次写的实现hosts文件修改的实现代码，支持功能有：

* 不破坏原有hosts文件，支持新host绑定或修改
* 支持host解绑

代码如下：

```java
/** 
 * 获取host文件路径 
 * @return 
 */ 
public static String getHostFile() { 
    String fileName = null; 
    // 判断系统 
    if ("linux".equalsIgnoreCase(System.getProperty("os.name"))) { 
        fileName = "/etc/hosts"; 
    } else { 
        fileName = System.getenv("windir") + "\\system32\\drivers\\etc\\hosts"; 
    } 
    return fileName; 
}

/** 
 * 根据输入IP和Domain，删除host文件中的某个host配置 
 * @param ip 
 * @param domain 
 * @return 
 */ 
public synchronized static boolean deleteHost(String ip, String domain) { 
    if (ip == null || ip.trim().isEmpty() || domain == null || domain.trim().isEmpty()) { 
        throw new IllegalArgumentException("ERROR： ip & domain must be specified"); 
    } 
    String splitter = " ";

    /** 
     * Step1: 获取host文件 
     */ 
    String fileName = getHostFile(); 
    List<?> hostFileDataLines = null; 
    try { 
        hostFileDataLines = FileUtils.readLines(new File(fileName)); 
    } catch (IOException e) { 
        System.out.println("Reading host file occurs error: " + e.getMessage()); 
        return false; 
    } 

    /** 
     * Step2: 解析host文件，如果指定域名不存在，则Ignore，如果已经存在，则直接删除该行配置 
     */ 
    List<String> newLinesList = new ArrayList<String>(); 
    // 标识本次文件是否有更新，比如如果指定的IP和域名已经在host文件中存在，则不用再写文件 
    boolean updateFlag = false; 
    for (Object line : hostFileDataLines) { 
        String strLine = line.toString(); 
        // 将host文件中的空行或无效行，直接去掉 
        if (StringUtils.isEmpty(strLine) || strLine.trim().equals("#")) { 
            continue; 
        } 
        // 如果没有被注释掉，则 
        if (!strLine.trim().startsWith("#")) { 
            strLine = strLine.replaceAll("", splitter); 
            int index = strLine.toLowerCase().indexOf(domain.toLowerCase()); 
            // 如果行字符可以匹配上指定域名，则针对该行做操作 
            if (index != -1) { 
                // 匹配到相同的域名，直接将整行数据干掉 
                updateFlag = true; 
                continue; 
            } 
        } 
        // 如果没有匹配到，直接将当前行加入代码中 
        newLinesList.add(strLine); 
    }

    /** 
     * Step3: 将更新写入host文件中去 
     */ 
    if (updateFlag) { 
        try { 
            FileUtils.writeLines(new File(fileName), newLinesList); 
        } catch (IOException e) { 
            System.out.println("Updating host file occurs error: " + e.getMessage()); 
            return false; 
        } 
    } 
    return true; 
}

/** 
 * 根据输入IP和Domain，更新host文件中的某个host配置 
 * @param ip 
 * @param domain 
 * @return 
 */ 
public synchronized static boolean updateHost(String ip, String domain) { 
    // Security.setProperty("networkaddress.cache.ttl", "0"); 
    // Security.setProperty("networkaddress.cache.negative.ttl", "0"); 
    if (ip == null || ip.trim().isEmpty() || domain == null || domain.trim().isEmpty()) { 
        throw new IllegalArgumentException("ERROR： ip & domain must be specified"); 
    } 
    String splitter = " ";

    /** 
     * Step1: 获取host文件 
     */ 
    String fileName = getHostFile(); 
    List<?> hostFileDataLines = null; 
    try { 
        hostFileDataLines = FileUtils.readLines(new File(fileName)); 
    } catch (IOException e) { 
        System.out.println("Reading host file occurs error: " + e.getMessage()); 
        return false; 
    }

    /** 
     * Step2: 解析host文件，如果指定域名不存在，则追加，如果已经存在，则修改IP进行保存 
     */ 
    List<String> newLinesList = new ArrayList<String>(); 
    // 指定domain是否存在，如果存在，则不追加 
    boolean findFlag = false; 
    // 标识本次文件是否有更新，比如如果指定的IP和域名已经在host文件中存在，则不用再写文件 
    boolean updateFlag = false; 
    for (Object line : hostFileDataLines) { 
        String strLine = line.toString(); 
        // 将host文件中的空行或无效行，直接去掉 
        if (StringUtils.isEmpty(strLine) || strLine.trim().equals("#")) { 
            continue; 
        } 
        if (!strLine.startsWith("#")) { 
            strLine = strLine.replaceAll("", splitter); 
            int index = strLine.toLowerCase().indexOf(domain.toLowerCase()); 
            // 如果行字符可以匹配上指定域名，则针对该行做操作 
            if (index != -1) { 
                // 如果之前已经找到过一条，则说明当前line的域名已重复， 
                // 故删除当前line, 不将该条数据放到newLinesList中去 
                if (findFlag) { 
                    updateFlag = true; 
                    continue; 
                } 
                // 不然，则继续寻找 
                String[] array = strLine.trim().split(splitter); 
                Boolean isMatch = false; 
                for (int i = 1; i < array.length; i++) { 
                    if (domain.equalsIgnoreCase(array[i]) == false) { 
                        continue; 
                    } else { 
                        findFlag = true; 
                        isMatch = true; 
                        // IP相同，则不更新该条数据，直接将数据放到newLinesList中去 
                        if (array[0].equals(ip) == false) { 
                            // IP不同，将匹配上的domain的ip 更新成设定好的IP地址 
                            StringBuilder sb = new StringBuilder(); 
                            sb.append(ip); 
                            for (int j = 1; i < array.length; i++) { 
                                sb.append(splitter).append(array[j]); 
                            } 
                            strLine = sb.toString(); 
                            updateFlag = true; 
                        } 
                    } 
                } 
            } 
        } 
        // 如果有更新，则会直接更新到strLine中去 
        // 故这里直接将strLine赋值给newLinesList 
        newLinesList.add(strLine); 
    }

    /** 
     * Step3: 如果没有任何Host域名匹配上，则追加 
     */ 
    if (!findFlag) { 
        newLinesList.add(new StringBuilder(ip).append(splitter).append(domain).toString()); 
    }

    /** 
     * Step4: 不管三七二十一，写设定文件 
     */ 
    if (updateFlag || !findFlag) { 
        try { 
            FileUtils.writeLines(new File(fileName), newLinesList); 
        } catch (IOException e) { 
            System.out.println("Updating host file occurs error: " + e.getMessage()); 
            return false; 
        } 
    } 
    return true; 
}
```

参考

[DNS in Java](https://www.ibm.com/developerworks/mydeveloperworks/blogs/738b7897-cd38-4f24-9f05-48dd69116837/entry/dns_in_java46?lang=en)
[DNS Caching in JVM](http://www.verisigninc.com/assets/stellent/030957.pdf)
[Java DNS Cache时效备忘录](http://kenwublog.com/java-dns-cache-setting)
[利用反射强制修改InetAddress类中的static变量addressCache](http://agilejava.blogbus.com/logs/6778674.html)