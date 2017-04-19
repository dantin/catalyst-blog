+++
date = "2016-08-10T14:20:21+08:00"
title = "Java Object的基本方法"
categories = ["Engineering"]
tags = ["Java"]
description = "本文记录Java Object的基本方法"
slug = "java-object"
+++

### 基本方法

| 方法名称    | 描述      |
| ---------- | -------- |
| equals()   | 判断两个对象是否相等 |
| hashCode() | 返回方法对象的散列值 |

__equals()__

Object类中默认的实现方式是:

```java
public boolean equals(Object obj) {
    return (this == obj);
}
```

只有`this`和`obj`引用同一个对象，才会返回`true`。

但实际上往往通过`equals()`来判断2个对象是否等价，而非验证它们的唯一性。这样，在实现自己的类时，就要重写`equals()`方法。

__equals()原理__

按照约定，`equals()`要满足以下规则。

* 自反性：`x.equals(x)`一定是`true`
* 对`null`：`x.equals(null)`一定是`false`
* 对称性：`x.equals(y)`和`y.equals(x)`结果一致
* 传递性：a equals b，b equals c，那么a也一定equals c。
* 一致性: 在某个运行时期间，2个对象的状态的改变不会不影响equals的决策结果，那么，在这个运行时期间，无论调用多少次equals，都返回相同的结果。

例子：

```java
class Test {
    private int num;
    private String data;

    public boolean equals(Object obj) {
        if (this == obj)
            return true;

        if ((obj == null) || (obj.getClass() != this.getClass()))
            return false;

        //能执行到这里，说明obj和this同类且非null。
        Test test = (Test) obj;
        return num == test.num&& (data == test.data || (data != null && data.equals(test.data)));
    }

    public int hashCode() {
        // 重写equals，也必须重写hashCode。具体后面介绍。
    }

}
```

Test类对象有2个字段，`num`和`data`，这2个字段代表了对象的状态，他们也用在`equals()`方法中作为评判的依据。

在第6行，传入的比较对象的引用和`this`做比较，这样做是为了节约执行时间，如果`this`和`obj`是 对同一个堆对象的引用，那么它们一定是`eqeuals()`的。

接着，判断`obj`是不是为`null`，如果为`null`，一定不`equals`，因为既然当前对象`this`能调用`equals()`方法，那么它一定不是`null`，非`null`和`null`当然不等价。

然后，比较2个对象的运行时类，是否为同一个类。不是同一个类，则不`equals()`。`getClass()`返回的是`this`和`obj`的运行时类的引用。如果它们属于同一个类，则返回的是同一个运行时类的引用。注意，一个类也是一个对象。

有些程序员使用下面的第二种写法替代第一种比较运行时类的写法。应该避免这样做。

```java
// 方法一：
if((obj == null) || (obj.getClass() != this.getClass())) 
    return false; 

// 方法二：
if(!(obj instanceof Test))
    return false; // avoid 避免！
```

它违反了公约中的对称原则。

```java
// 假设Dog扩展了Aminal类。
dog instanceof Animal      // 得到true
animal instanceof Dog      // 得到false
```

这就会导致

```java
animal.equls(dog)   // 返回true
dog.equals(animal)  // 返回false
```

仅当Test类没有子类的时候，这样做才能保证是正确的。

按照第一种方法实现，那么equals只能比较同一个类的对象，不同类对象永远是false。但这并不是强制要求的。一般我们也很少需要在不同的类之间使用equals。

__equals()实现注意事项__

1. 在具体比较对象的字段的时候，对于基本值类型的字段，直接用`==`来比较（注意浮点数的比较，这是一个坑）
2. 对于引用类型的字段，可以调用他们的`equals()`，当然，也需要处理字段为`null`的情况。
3. 对于浮点数的比较，我在看Arrays.binarySearch的源代码时，发现了如下对于浮点数的比较的技巧： 

    ```java
    if ( Double.doubleToLongBits(d1) == Double.doubleToLongBits(d2) ) //d1 和 d2 是double类型

    if(  Float.floatToIntBits(f1) == Float.floatToIntBits(f2)  )      //f1 和 f2 是d2是float类型
    ```

    并不总是要将对象的所有字段来作为`equals()`的评判依据，这取决于业务要求。

4. 最后需要注意的是，`equals()`方法的参数类型是Object，不要写错！

__hashCode()__

这个方法返回对象的散列码，返回值是int类型的散列码。对象的散列码是为了更好的支持基于哈希机制的Java集合类，例如：`Hashtable, HashMap, HashSet`等。

__原理__

关于`hashCode()`方法，一致的约定是：

* 重写了`equals()`方法的对象必须同时重写`hashCode()`方法。
* 如果两个对象通过`equals()`调用后返回是`true`，那么这两个对象的`hashCode()`方法也必须返回同样的`int`型散列码
* 如果两个对象通过`equals()`返回`false`，它们的`hashCode()`返回的值允许相同。(`hashCode()`返回独一无二的散列码，会让存储这个对象的`hashtables`更好地工作。)

在上面的例子中，Test类对象有两个字段，`num`和`data`，这两个字段代表了对象的状态，它们也用在`equals()`方法中作为评判的依据。那么， 在`hashCode()`方法中，这两个字段也要参与hash值的运算，作为hash运算的中间参数。这点很关键，这是为了遵守：__两个对象equals，那么 hashCode一定相同__规则。

也是说，参与equals函数的字段，也必须都参与hashCode 的计算。

合乎情理的是：同一个类中的不同对象返回不同的散列码。

典型的方式就是根据对象的地址来转换为此对象的散列码，但是这种方式对于Java来说并不是唯一的要求的的实现方式。通常也不是最好的实现方式。

相比于`equals()`公认实现约定，`hashCode()`的公约要求是很容易理解的。有两个重点是hashCode方法必须遵守的。约定的第三点，其实就是第二点的细化，下面我们就来看看对hashCode方法的一致约定要求。


1. 在某个运行时期间，只要对象的（字段的）变化不会影响`equals()`方法的决策结果，那么，在这个期间，无论调用多少次`hashCode()`，都必须返回同一个散列码。
2. 通过`equals()`调用返回`true`的两个对象的`hashCode()`一定一样。
3. 通过`equasl()`返回`false`的两个对象的散列码不需要不同，也就是它们的`hashCode()`方法的返回值允许出现相同的情况。

总之：__等价的(调用equals返回true)对象必须产生相同的散列码。不等价的对象，不要求产生的散列码不相同。__

__hashCode()编写指导__

在编写`hashCode()`时，需要考虑的是，最终的hash是个int值，而不能溢出。不同的对象的hash码应该尽量不同，避免hash冲突。

解决方案如下：

定义一个int类型的变量 hash,初始化为 7。

接下来把认为重要的字段（`equals()`中衡量相等的字段）参入散列运，算每一个重要字段都会产生一个hash分量，为最终的hash值做出贡献（影响）

运算方法参考表

| 字段类型           | hash分量                                                                         |
| ----------------- | ------------------------------------------------------------------------------- |
| byte, char, short | int (int)var                                                                    |
| long              | (int)(var ^ (var >>> 32))                                                       |
| boolean           | var ? 1:0                                                                       |
| float             | Float.floatToIntBits(var)                                                       |
| double            | long bits = Double.doubleToLongBits(var); weight = (int)(bits ^ (bits >>> 32)); |
| 引用类型           | (null == var ? 0 : var.hashCode())                                              |
 
最后把所有的分量都总和起来，注意并不是简单的相加。选择一个倍乘的数字31，参与计算。然后不断地递归计算，直到所有的字段都参与了。

```java
int hash = 7;
hash = 31 * hash + 字段1贡献分量;
hash = 31 * hash + 字段2贡献分量;
.....

return hash；
```

### 多线程相关

| 方法名称         | 描述      |
| --------------- | -------- |
| notify()        | 通知一个在对象上等待的线程，使其从wait()方法返回，而返回的前提是该线程获取到了对象的锁 |
| notifyAll()     | 通知所有等待在该对象上的线程 |
| wait()          | 调用该方法的线程进入WAITING状态，只有等待另外线程的通知或被中断才会返回，需要注意，调用wait()方法后，会释放对象的锁 |
| wait(long)      | 超时等待一段时间，这里的参数时间是毫秒，也就是等待长达n毫秒，如果没有通知就超时返回 |
| wait(long, int) | 对于超时时间更细粒度的控制，可以达到纳秒 |

