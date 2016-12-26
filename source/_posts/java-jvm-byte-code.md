---
title: 深入理解Java虚拟机之七：字节码指令简介
date: 2016-06-22 10:13:09
categories: 学术
tags: [Java, JVM]
toc: true
---

Java虚拟机指令是由操作码Opcode（占用一个字节长度、代表某种特定操作含义的数字），以及跟随在其后的零至多个代表此操作所需参数的称为操作数Operands构成的。由于Java虚拟机是面向操作数栈而不是寄存器的架构，所以大多数指令都只有操作码，而没有操作数。

字节码指令集是一种具有鲜明特点、优劣势都很突出的指令集架构：

* 由于限定了Java虚拟机__操作码的长度为1个字节__，指令集的操作码不能超过256条。
* Class文件格式放弃了编译后代码中__操作数长度对齐__，这就意味者虚拟机处理那些超过一个字节数据的时候，不得不在运行的时候从字节码中重建出具体数据的结构。

这种操作在一定程度上会降低一些性能，但这样做的优势也非常的明显：

* 放弃了操作数长度对齐，就意味着可以省略很多填充和间隔符号
* 用一个字节来表示操作码，也是为了获取短小精悍的代码。

这种追求尽可能小数据量，高传输效率的设计是由Java语言之初面向网络、智能家电技术背景决定的。

Java虚拟机解释器执行简单模型如下：

```
do{
    计算PC寄存器的值+1;
    根据PC寄存器只是位置，从字节码流中取出操作码;
    if(存在操作数)
        从字节码中取出操作数;
    执行操作码定义的操作;
}while(字节码长度>0);
```

### 字节码与数据类型

在Java虚拟机指令集中，大多数的指令都包含了其操作所对应的数据类型信息。例如，iload指令用于从局部变量表中加载int型的数据到操作数栈中。

但是由于虚拟机操作码长度只有一个字节，所以包含了数据类型的操作码就为指令集的设计带来了很大的压力：如果每一种数据类型相关的指令都支持Java虚拟机所有运行时数据类型的话，那指令集的数据就会超过256个了。

因此虚拟机只提供了有限的指令集来支持所有的数据类型。如load操作，只有iload、lload、fload、dload、aload用来支持int、long、float、double、reference类型的入栈，而对于boolean、byte、short和char则没有专门的指令来进行运算。编译器会在编译期或运行期将byte和short类型的数据带符号扩展为int类型的数据，将boolean和char类型的数据零位扩展为相应的int类型数据。与之类似，在处理boolean、byte、short和char类型的数组时，也会发生转换。因此，大多数对应于boolean、byte、short和char类型数据的操作，实际上都是使用相应的int类型作为运算类型。

### 指令类型

#### 加载和存储指令

加载和存储指令用于将数据从栈帧的局部变量表和操作数栈之间来回传输。

1. 将一个局部变量加载到操作数栈的指令：
    `iload,iload_<n>,lload,lload_<n>,fload,fload_<n>,dload,dload_<n>,aload,aload_<n>`；
2. 将一个数值从操作数栈存储到局部变量表的指令：
    `istore,istore_<n>,lstore,lstore_<n>,fstore,fstore_<n>,dstore,dstore_<n>,astore,astore_<n>`；
3. 将常量加载到操作数栈的指令：
    `bipush,sipush,ldc,ldc_w,ldc2_w,aconst_null,iconst_ml,iconst_<i>,lconst_<l>,fconst_<f>,dconst_<d>`；
4. 局部变量表的访问索引指令：
    `wide`；

一部分以尖括号结尾的指令代表了一组指令，如`iload_<i>`，代表了`iload_0, iload_1`等，这几组指令都是带有一个操作数的通用指令。

#### 运算指令

算术指令用于对两个操作数栈上的值进行某种特定运算，并把结果重新存入到操作栈顶。

1. 加法指令：iadd,ladd,fadd,dadd
2. 减法指令：isub,lsub,fsub,dsub
3. 乘法指令：imul,lmul,fmul,dmul
4. 除法指令：idiv,ldiv,fdiv,ddiv
5. 求余指令：irem,lrem,frem,drem
6. 取反指令：ineg,leng,fneg,dneg
7. 位移指令：ishl,ishr,iushr,lshl,lshr,lushr
8. 按位或指令：ior,lor
9. 按位与指令：iand,land
10. 按位异或指令：ixor,lxor
11. 局部变量自增指令：iinc
12. 比较指令：dcmpg,dcmpl,fcmpg,fcmpl,lcmp

Java虚拟机没有明确规定整型数据溢出的情况，但规定了处理整型数据时，只有除法和求余指令出现除数为0时会导致虚拟机抛出异常。

Java虚拟机要求在浮点数运算的时候，所有结果否必须舍入到适当的精度，如果有两种可表示的形式与该值一样，会优先选择最低有效位为零的，称之为“最接近数舍入模式”。

浮点数向整数转换的时候，Java虚拟机使用IEEE 754标准中的向零舍入模式，这种模式舍入的结果会导致数字被截断，所有小数部分的有效字节会被丢掉。

#### 类型转换指令

类型转换指令将两种Java虚拟机数值类型相互转换，这些操作一般用于实现用户代码的__显式类型转换__操作。

JVM直接就支持宽化类型转换(小范围类型向大范围类型转换)：

1. int类型到long,float,double类型
2. long类型到float,double类型
3. float到double类型

但在处理__窄化类型转换__时，必须显式使用转换指令来完成，这些指令包括：i2b、i2c、i2s、l2i、f2i、f2l、d2i、d2l和 d2f。

将int或long窄化为整型T的时候，仅仅简单的把除了低位的N个字节以外的内容丢弃，N是T的长度。这有可能导致转换结果与输入值有不同的正负号。

在将一个浮点值窄化为整数类型T（仅限于int和long类型），将遵循以下转换规则：

1. 如果浮点值是NaN，则转换结果就是int或long类型的0
2. 如果浮点值不是无穷大，浮点值使用IEEE 754的向零舍入模式取整，获得整数v，如果v在T表示范围之内，那就过就是v
3. 否则，根据v的符号，转换为T所能表示的最大或者最小正数

#### 对象创建与访问指令

虽然类实例和数组都是对象，Java虚拟机对类实例和数组的创建与操作使用了不同的字节码指令。

1. 创建实例的指令：
    new
2. 创建数组的指令：
    newarray,anewarray,multianewarray
3. 访问字段指令：
    getfield,putfield,getstatic,putstatic
4. 把数组元素加载到操作数栈指令：
    baload,caload,saload,iaload,laload,faload,daload,aaload
5. 将操作数栈的数值存储到数组元素中执行：
    bastore,castore,castore,sastore,iastore,fastore,dastore,aastore
6. 取数组长度指令：
    arraylength
7. 检查实例类型指令：
    instanceof,checkcast



#### 操作数栈管理指令

如同操作一个普通数据结构中的堆栈那样，Java虚拟机提供了一些用于直接操作操作数栈的指令，包括：

1. 将操作数栈的栈顶一个或两个元素出栈：
    pop,pop2
2. 复制栈顶一个或两个数值并将复制值或双份的复制值重新压入栈顶：
    dup,dup2,dup_x1,dup2_x1,dup_x2,dup2_x2
3. 将栈最顶端的两个数值互换：
    swap

#### 控制转移指令

让JVM有条件或无条件从指定指令而不是控制转移指令的下一条指令继续执行程序。控制转移指令包括：

1. 条件分支：ifeq,iflt,ifle,ifne,ifgt,ifge,ifnull,ifnotnull,if_cmpeq,if_icmpne,if_icmlt,if_icmpgt等
2. 复合条件分支：tableswitch,lookupswitch
3. 无条件分支：goto,goto_w,jsr,jsr_w,ret

JVM中有专门的指令集处理int和reference类型的条件分支比较操作，为了可以无明显标示一个实体值是否是null,有专门的指令检测null值。boolean类型和byte类型,char类型和short类型的条件分支比较操作，都使用int类型的比较指令完成，而long,float,double条件分支比较操作，由相应类型的比较运算指令，运算指令会返回一个整型值到操作数栈中，随后再执行int类型的条件比较操作完成整个分支跳转。各种类型的比较都最终会转化为int类型的比较操作。

#### 方法调用和返回指令

* invokevirtual指令：调用对象的实例方法，根据对象的实际类型进行分派(虚拟机分派)。
* invokeinterface指令：调用接口方法，在运行时搜索一个实现这个接口方法的对象，找出合适的方法进行调用。
* invokespecial：调用需要特殊处理的实例方法，包括实例初始化方法，私有方法和父类方法
* invokestatic：调用类方法(static)

方法返回指令是根据返回值的类型区分的，包括ireturn(返回值是boolean,byte,char,short和 int),lreturn,freturn,drturn和areturn，另外一个return供void方法，实例初始化方法，类和接口的类初始化i方法使用。

#### 异常处理指令

在Java程序中显式抛出异常的操作（throw语句）都有athrow指令来实现，除了用throw语句显示抛出异常情况外，Java虚拟机规范还规定了许多运行时异常会在其他Java虚拟机指令检测到异常状况时自动抛出。

在Java虚拟机中，处理异常不是由字节码指令来实现的，而是采用异常表来完成的。

#### 同步指令

JVM支持方法级同步和方法内部一段指令序列同步，这两种都是通过moniter实现的。

* 方法级的同步是隐式的，无需通过字节码指令来控制，它实现在方法调用和返回操作中。虚拟机从方法常量池中的方法标结构中的ACC_SYNCHRONIZED标志区分是否是同步方法。方法调用时，调用指令会检查该标志是否被设置，若设置，执行线程持有moniter，然后执行方法，最后完成方法时释放moniter。
* 同步一段指令集序列，通常由synchronized块标示，JVM指令集中有monitorenter和monitorexit来支持synchronized语义。

结构化锁定是指方法调用期间每一个monitor退出都与前面monitor进入相匹配的情形。JVM通过以下两条规则来保证结结构化锁成立(T代表一线程，M代表一个monitor)：

1. T在方法执行时持有M的次数必须与T在方法完成时释放的M次数相等
2. 任何时刻都不会出现T释放M的次数比T持有M的次数多的情况
