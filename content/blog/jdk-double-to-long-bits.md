+++
date = "2016-11-14T15:07:27+08:00"
title = "Double to Long Bits"
categories = ["Engineering"]
tags = ["Java", "JDK"]
description = "本文介绍JDK内部Double类型转Long型的实现方法"
slug = "jdk-double-to-long-bits"
+++

把一个Double类型转成Long类型。

### JDK实现

这部分源码在java.lang.Double中。

```java
public static long doubleToLongBits(double value) {
    long result = doubleToRawLongBits(value);
    // Check for NaN based on values of bit fields, maximum
    // exponent and nonzero significand.
    if ( ((result & DoubleConsts.EXP_BIT_MASK) ==
          DoubleConsts.EXP_BIT_MASK) &&
         (result & DoubleConsts.SIGNIF_BIT_MASK) != 0L)
        result = 0x7ff8000000000000L;
    return result;
}
```

### 分析

DoubleConsts的定义在sun.misc中

```java
public class DoubleConsts {
    ...
    public static final long EXP_BIT_MASK = 9218868437227405312L;
    public static final long SIGNIF_BIT_MASK = 4503599627370495L;
    ...
}
```

把Long型转化成Byte Array：

```java
import java.nio.ByteBuffer;

public class Demo {
    public static void main(String[] args) {
        Long mis = 4503599627370495L;
        Long mis2 = 9218868437227405312L;
        System.out.println(javax.xml.bind.DatatypeConverter.printHexBinary(longToBytes(mis)));
        System.out.println(javax.xml.bind.DatatypeConverter.printHexBinary(longToBytes(mis2)));
    }

    public static byte[] longToBytes(long x) {
        ByteBuffer buffer = ByteBuffer.allocate(Long.BYTES);
        buffer.putLong(x);
        return buffer.array();
    }
}
```

输出：

```console
000FFFFFFFFFFFFF
7FF0000000000000
```

Double类型的Bit模式：

```console
Bit 63 (the bit that is selected by the mask {@code 0x8000000000000000L})
   represents the sign of the floating-point number. 
Bits 62-52 (the bits that are selected by the mask {@code 0x7ff0000000000000L})
   represent the exponent.
Bits 51-0 (the bits that are selected by the mask {@code 0x000fffffffffffffL})
   represent the significand (sometimes called the mantissa) of the floating-point 
   number.
```

Double的NaN定义：

```java
/**
 * A constant holding a Not-a-Number (NaN) value of type
 * {@code double}. It is equivalent to the value returned by
 * {@code Double.longBitsToDouble(0x7ff8000000000000L)}.
 */
public static final double NaN = 0.0d / 0.0;
```

以上定义了一个常量型的NaN，它的效果和Double.longBitsToDouble(0x7ff8000000000000L)的返回值是一样的，我们可以看看Double.longBitsToDouble中的定义：

```console
If the argument is any value in the range 0x7ff0000000000001L through 0x7fffffffffffffffL or in the range 0xfff0000000000001L through 0xffffffffffffffffL, the result is a NaN. No IEEE 754 floating-point operation provided by Java can distinguish between two NaN values of the same type with different bit patterns.
```

如上可知，二进制的0x7ff0000000000001L~0x7fffffffffffffffL 和 0xfff0000000000001L~0xffffffffffffffffL 之间的数值是被定义成NaN类型，类似正无穷大和负无穷大，但又有区别。

在Float中也类似。