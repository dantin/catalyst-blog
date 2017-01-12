+++
date = "2016-09-30T16:39:44+08:00"
title = "Java中Fail Fast和Fail Safe的区别"
categories = ["Engineering"]
tags = ["Java"]
description = "本文讨论并发修改的两种机制"
slug = "java-fail-fast-iterator-vs-fail-safe-iterator"
+++

Fail Fast和Fail Safe是并发修改的两种机制。

在详细讨论这两种机制的区别之前，首先得先了解并发修改。

### 什么是并发修改

当一个或多个线程正在遍历一个集合Collection，此时另一个线程修改了这个集合的内容（添加，删除或者修改）。这就是并发修改。

### 什么是Fail Fast机制

Fail Fast机制在遍历一个集合时，当集合结构被修改，会抛出Concurrent Modification Exception。

Fail Fast会在以下两种情况下抛出ConcurrentModificationException：

#### 单线程环境

集合被创建后，在遍历它的过程中修改了结构。

__注意__：remove()方法会让expectModcount和modcount 相等，所以是不会抛出这个异常。

#### 多线程环境

当一个线程在遍历这个集合，而另一个线程对这个集合的结构进行了修改。

注意，迭代器的快速失败行为无法得到保证，因为一般来说，不可能对是否出现不同步并发修改做出任何硬性保证。快速失败迭代器会尽最大努力抛出ConcurrentModificationException。因此，为提高这类迭代器的正确性而编写一个依赖于此异常的程序是错误的做法：迭代器的快速失败行为应该仅用于检测Bug。

### Fail Fast机制是如何检测的

迭代器在遍历过程中是直接访问内部数据的，因此内部的数据在遍历的过程中无法被修改。为了保证不被修改，迭代器内部维护了一个标记 “mode” ，当集合结构改变（添加删除或者修改），标记"mode"会被修改，而迭代器每次的hasNext()和next()方法都会检查该"mode"是否被改变，当检测到被修改时，抛出Concurrent Modification Exception。

下面看看ArrayList迭代器部分的源码

```java
private class Itr implements Iterator<E> {
    int cursor;
    int lastRet = -1;
    int expectedModCount = ArrayList.this.modCount;

    public boolean hasNext() {
        return (this.cursor != ArrayList.this.size);
    }

    public E next() {
        checkForComodification();
        /** 省略此处代码 */
    }

    public void remove() {
        if (this.lastRet < 0)
            throw new IllegalStateException();
        checkForComodification();
        /** 省略此处代码 */
    }

    final void checkForComodification() {
        if (ArrayList.this.modCount == this.expectedModCount)
            return;
        throw new ConcurrentModificationException();
    }
}
```

可以看到它的标记“mode”为expectedModeCount

### Fail Safe机制

Fail Safe任何对集合结构的修改都会在一个复制的集合上进行修改，因此不会抛出ConcurrentModificationException

Fail Safe机制有两个问题：

* 需要复制集合，产生大量的无效对象，开销大
* 无法保证读取的数据是目前原始数据结构中的数据。

### Fail Fast和Fail Safe例子

#### Fail Fast

```java
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

public class FailFastExample {

    public static void main(String[] args) {
        Map<String, String> premiumPhone = new HashMap<>();
        premiumPhone.put("Apple", "iPhone");
        premiumPhone.put("HTC", "HTC One");
        premiumPhone.put("Samsung", "S5");

        Iterator iterator = premiumPhone.keySet().iterator();

        while (iterator.hasNext()) {
            System.out.println(premiumPhone.get(iterator.next()));
            premiumPhone.put("Sony", "Xperia Z");
        }
    }

}
```

输出

```bash
iPhone
Exception in thread "main" java.util.ConcurrentModificationException
    at java.util.HashMap$HashIterator.nextNode(HashMap.java:1429)
    at java.util.HashMap$KeyIterator.next(HashMap.java:1453)
    at FailFastExample.main(FailFastExample.java:16)
```

#### Fail Safe

```java
import java.util.concurrent.ConcurrentHashMap;
import java.util.Iterator;
import java.util.Map;

public class FailSafeExample {

    public static void main(String[] args) {
        Map<String, String> premiumPhone = new ConcurrentHashMap<>();
        premiumPhone.put("Apple", "iPhone");
        premiumPhone.put("HTC", "HTC One");
        premiumPhone.put("Samsung", "S5");

        Iterator iterator = premiumPhone.keySet().iterator();

        while (iterator.hasNext()) {
            System.out.println(premiumPhone.get(iterator.next()));
            premiumPhone.put("Sony", "Xperia Z");
        }
    }

}
```

输出

```bash
iPhone
HTC One
S5
```

### Fail Fast和Fail Safe的区别

|                                        | Fail Fast Iterator | Fail Safe Iterator |
| -------------------------------------- | ------------------ | ------------------ |
| Throw ConcurrentModification Exception | Yes                | No                 |
| Clone object                           | No                 | Yes                |
| Memory Overhead                        | No                 | Yes                |
| Examples                 | HashMap,Vector,ArrayList,HashSet | CopyOnWriteArrayList, ConcurrentHashMap |

参考

[Java Hungry](http://javahungry.blogspot.com/2014/04/fail-fast-iterator-vs-fail-safe-iterator-difference-with-example-in-java.html)
