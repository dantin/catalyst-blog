+++
date = "2016-09-28T17:15:08+08:00"
title = "Java Finally解析"
categories = ["Engineering"]
tags = ["Java"]
description = "本文记录Java finally语句对返回值的影响"
slug = "java-finally-internal"
+++

Java finally内的处理在什么情况下会影响到返回值？

这是初学者经常碰到的一个问题，分析如下。

### 问题

#### 整型

下面代码，返回什么值？

```java
public static int x() {
    int i = 0;

    try {
        i = 5;
        return i;
    } finally {
        i = 10;
    }
}
```

答案：5。

思考一秒钟，Why？

首先需要明确的是，Java底层是值传递。

查看字节码，发现finally复制了一个i，对它的修改不会影响之前的返回值。

```bash
public static int x();
Code:
   0: iconst_0
   1: istore_0
   2: iconst_5
   3: istore_0
   4: iload_0
   5: istore_1
   6: bipush        10
   8: istore_0
   9: iload_1
  10: ireturn
  11: astore_2
  12: bipush        10
  14: istore_0
  15: aload_2
  16: athrow
Exception table:
   from    to  target type
       2     6    11   any
```

第5行保存到本地变量1，第9行又把本地变量1中的内容取回并返回。

#### 字符串

那么如果操作的是字符串呢？

```java
public static String str() {
    String s = "";

    try {
        s = "a";
        return s;
    } finally {
        s = "a" + "b";
    }
}
```

返回：a

字符串存储在常量池，try语句中返回的是常量池的引用，finally中的修改只是修改了复制的值。

#### 对象

如果操作的是引用的成员呢？

```java
public static StringBuffer sb() {
    StringBuffer sb = new StringBuffer("");

    try {
        sb = new StringBuffer("a");
        return sb;
    } finally {
        sb.append("b");
    }
}
```

返回：ab

try语句中返回的是引用，finally中的修改了复制引用的成员，因此有影响。

### 总结

* finally{}的执行时间是在try{}中间的return返回之后；
* finally中的修改只是修改了复制的值；
* Java的底层实现是值传递；
