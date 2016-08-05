title: Spring AOP实现原理与CGLIB应用
date: 2016-08-04 15:46:28
categories: 工程
tags: [Spring]
toc: true
---

AOP（Aspect Orient Programming），作为面向对象编程的一种补充，广泛应用于处理一些具有横切性质的系统级服务，如事务管理、安全检查、缓存、对象池管理等。AOP实现的关键就在于AOP框架自动创建的AOP代理，AOP代理则可分为静态代理和动态代理两大类，其中静态代理是指使用AOP框架提供的命令进行编译，从而在编译阶段就可生成AOP代理类，因此也称为编译时增强；而动态代理则在运行时借助于JDK动态代理、CGLIB等在内存中“临时”生成AOP动态代理类，因此也被称为运行时增强。

### AOP的存在价值

在传统OOP编程里以对象为核心，整个软件系统由系列相互依赖的对象所组成，而这些对象将被抽象成一个一个的类，并允许使用类继承来管理类与类之间一般到特殊的关系。随着软件规模的增大，应用的逐渐升级，慢慢出现了一些OOP很难解决的问题。
我们可以通过分析、抽象出一系列具有一定属性与行为的对象，并通过这些对象之间的协作来形成一个完整的软件功能。由于对象可以继承，因此我们可以把具有相同功能或相同特性的属性抽象到一个层次分明的类结构体系中。随着软件规范的不断扩大，专业化分工越来越系列，以及OOP应用实践的不断增多，随之也暴露出了一些OOP无法很好解决的问题。

现在假设系统中有3段完全相似的代码，这些代码通常会采用“复制”、“粘贴”方式来完成，通过这种“复制”、“粘贴”方式开发出来的软件如图1所示。

![多个地方包含相同代码的软件](/images/spring-aop-001.jpg "Spring-aop-001")

看到如图1所示的示意图，可能有的读者已经发现了这种做法的不足之处：如果有一天，图1中的深色代码段需要修改，那是不是要打开3个地方的代码进行修改？如果不是3个地方包含这段代码，而是100个地方，甚至是1000个地方包含这段代码段，那会是什么后果？

为了解决这个问题，我们通常会采用将如图1所示的深色代码部分定义成一个方法，然后在3个代码段中分别调用该方法即可。在这种方式下，软件系统的结构如图2所示。

![通过方法调用实现系统功能](/images/spring-aop-002.jpg "Spring-aop-002")

对于如图2所示的软件系统，如果需要修改深色部分的代码，只要修改一个地方即可，不管整个系统中有多少地方调用了该方法，程序无须修改这些地方，只需修改被调用的方法即可——通过这种方式，大大降低了软件后期维护的复杂度。

对于如图2所示的方法1、方法2、方法3依然需要显式调用深色方法，这样做能够解决大部分应用场景。但对于一些更特殊的情况：应用需要方法1、方法2、方法3彻底与深色方法分离——方法1、方法2、方法3无须直接调用深色方法，那如何解决？

因为软件系统需求变更是很频繁的事情，系统前期设计方法1、方法2、方法3时只实现了核心业务功能，过了一段时间，我们需要为方法1、方法2、方法3都增加事务控制；又过了一段时间，客户提出方法1、方法2、方法3需要进行用户合法性验证，只有合法的用户才能执行这些方法；又过了一段时间，客户又提出方法1、方法2、方法3应该增加日志记录；又过了一段时间，客户又提出……面对这样的情况，我们怎么办？通常有两种做法：

* 根据需求说明书，直接拒绝客户要求。
* 拥抱需求，满足客户的需求。
第一种做法显然不好，客户是上帝，我们应该尽量满足客户的需求。通常会采用第二种做法，那如何解决呢？是不是每次先定义一个新方法，然后修改方法1、方法2、方法3，增加调用新方法？这样做的工作量也不小啊！我们希望有一种特殊的方法：我们只要定义该方法，无须在方法1、方法2、方法3中显式调用它，系统会“自动”执行该特殊方法。

上面想法听起来很神奇，甚至有一些不切实际，但其实是完全可以实现的，实现这个需求的技术就是AOP。AOP专门用于处理系统中分布于各个模块（不同方法）中的交叉关注点的问题，在Java EE应用中，常常通过AOP来处理一些具有横切性质的系统级服务，如事务管理、安全检查、缓存、对象池管理等，AOP已经成为一种非常常用的解决方案。

### 使用AspectJ的编译时增强进行AOP

AspectJ是一个基于Java语言的AOP框架，提供了强大的AOP功能，其他很多AOP框架都借鉴或采纳其中的一些思想。

AspectJ是Java语言的一个AOP实现，其主要包括两个部分：第一个部分定义了如何表达、定义AOP编程中的语法规范，通过这套语言规范，我们可以方便地用AOP来解决Java语言中存在的交叉关注点问题；另一个部分是工具部分，包括编译器、调试工具等。

AspectJ是最早、功能比较强大的AOP实现之一，对整套AOP机制都有较好的实现，很多其他语言的AOP实现，也借鉴或采纳了AspectJ中很多设计。在Java领域，AspectJ中的很多语法结构基本上已成为AOP领域的标准。

下载、安装AspectJ比较简单，读者登录[AspectJ官网](http://www.eclipse.org/aspectj)，即可下载到一个可执行的JAR包，使用`java -jar aspectj-1.x.x.jar`命令、多次单击“Next”按钮即可成功安装AspectJ。

成功安装了AspectJ之后，将会在E:\Java\AOP\aspectj1.6路径下（AspectJ 的安装路径）看到如下文件结构：

* bin：该路径下存放了aj、aj5、ajc、ajdoc、ajbrowser等命令，其中ajc命令最常用，它的作用类似于javac，用于对普通Java类进行编译时增强。
* docs：该路径下存放了AspectJ的使用说明、参考手册、API文档等文档。
*lib：该路径下的4个JAR文件是AspectJ的核心类库。
* 相关授权文件。

一些文档、AspectJ入门书籍，一谈到使用AspectJ，就认为必须使用Eclipse工具，似乎离开了该工具就无法使用AspectJ了。

虽然AspectJ是Eclipse基金组织的开源项目，而且提供了Eclipse的AJDT插件（AspectJ Development Tools）来开发AspectJ应用，但AspectJ绝对无须依赖于Eclipse工具。

实际上，AspectJ的用法非常简单，就像我们使用JDK编译、运行Java程序一样。下面通过一个简单的程序来示范AspectJ的用法，并分析AspectJ如何在编译时进行增强。

首先编写一个简单的Java类，这个Java类用于模拟一个业务组件。

```java
public class Hello {
    // 定义一个简单方法，模拟应用中的业务逻辑方法
    public void sayHello(){System.out.println("Hello AspectJ!");}
    // 主方法，程序的入口
    public static void main(String[] args)
    {
        Hello h = new Hello();
        h.sayHello();
    }
}
```

上面Hello类模拟了一个业务逻辑组件，编译、运行该Java程序，这个结果是没有任何悬念的，程序将在控制台打印“Hello AspectJ”字符串。

假设现在客户需要在执行sayHello()方法之前启动事务，当该方法执行结束时关闭事务，在传统编程模式下，我们必须手动修改sayHello()方法——如果改为使用AspectJ，则可以无须修改上面的sayHello()方法。

下面我们定义一个特殊的Java类。

```java
public aspect TxAspect{
    // 指定执行 Hello.sayHello() 方法时执行下面代码块
    void around():call(void Hello.sayHello()){
        System.out.println("开始事务 ...");
        proceed();
        System.out.println("事务结束 ...");
    }
        
}
```

可能读者已经发现了，上面类文件中不是使用class、interface、enum在定义Java类，而是使用了aspect——难道Java语言又新增了关键字？没有！上面的TxAspect根本不是一个Java类，所以aspect也不是Java支持的关键字，它只是AspectJ才能识别的关键字。

上面粗体字代码也不是方法，它只是指定当程序执行Hello对象的sayHello()方法时，系统将改为执行花括号代码块，其中proceed()代表回调原来的sayHello()方法。

正如前面提到的，Java无法识别TxAspect.java文件的内容，所以我们要使用ajc.exe命令来编译上面的Java程序。为了能在命令行使用ajc.exe命令，需要把AspectJ安装目录下的bin路径（比如`E:\Java\AOP\aspectj1.6\bin`目录）添加到系统的PATH环境变量中。接下来执行如下命令进行编译：

```bash
# ajc -d . Hello.java TxAspect.java
ajc -d . -aspectpath $(brew --prefix aspectj)/libexec/aspectj/lib/aspectjrt.jar Hello.java TxAspect.java
```

我们可以把ajc.exe理解成javac.exe命令，都用于编译Java程序，区别是ajc.exe命令可识别AspectJ的语法；从这个意义上看，我们可以将ajc.exe当成一个增强版的javac.exe命令。

运行该Hello类依然无须任何改变，因为Hello类位于default包下。程序使用如下命令运行Hello类：

```bash
# java Hello
java -cp $(brew --prefix aspectj)/libexec/aspectj/lib/aspectjrt.jar:. Hello
```

运行该程序，将看到一个令人惊喜的结果：

```bash
开始事务 ...
Hello AspectJ!
事务结束 ...
```

从上面运行结果来看，我们完全可以不对Hello.java类进行任何修改，同时又可以满足客户的需求：上面程序只是在控制台打印“开始事务 ...”、“结束事务 ...”来模拟了事务操作，实际上我们可用实际的事务操作代码来代替这两行简单的语句，这就可以满足客户需求了。

如果客户再次提出新需求，需要在sayHello()方法后增加记录日志的功能，那也很简单，我们再定义一个LogAspect，程序如下：

```java
public aspect LogAspect {
    // 定义一个 PointCut，其名为 logPointcut
    // 该 PointCut 对应于指定 Hello 对象的 sayHello 方法
    pointcut logPointcut():execution(void Hello.sayHello());
    // 在 logPointcut 之后执行下面代码块
    after():logPointcut() {
        System.out.println("记录日志 ...");
    }
}
```

上面程序的粗体字代码定义了一个Pointcut：logPointcut。等同于执行Hello对象的sayHello()方法，并指定在logPointcut之后执行简单的代码块，也就是说，在sayHello()方法之后执行指定代码块。使用如下命令来编译上面的Java程序：

```bash
# ajc -d . *.java
ajc -d . -aspectpath $(brew --prefix aspectj)/libexec/aspectj/lib/aspectjrt.jar Hello.java TxAspect.java LogAspect.java
```

再次运行Hello类，将看到如下运行结果：

```bash
开始事务 ...
Hello AspectJ!
记录日志 ...
事务结束 ...
```

从上面运行结果来看，通过使用AspectJ提供的AOP支持，我们可以为sayHello()方法不断增加新功能。

为什么在对Hello类没有任何修改的前提下，而Hello类能不断地、动态增加新功能呢？这看上去并不符合Java基本语法规则啊。实际上我们可以使用Java的反编译工具来反编译前面程序生成的Hello.class文件，发现Hello.class文件的代码如下：

```java
import java.io.PrintStream;
import org.aspectj.runtime.internal.AroundClosure;

public class Hello { 
  public void sayHello() {
    try {
      System.out.println("Hello AspectJ!"); } catch (Throwable localThrowable) {
      LogAspect.aspectOf().ajc$after$lee_LogAspect$1$9fd5dd97(); throw localThrowable; }
      LogAspect.aspectOf().ajc$after$lee_LogAspect$1$9fd5dd97();
    }

    ...

    private static final void sayHello_aroundBody1$advice(Hello target,
             TxAspect ajc$aspectInstance, AroundClosure ajc$aroundClosure) {
      System.out.println("开始事务 ...");
      AroundClosure localAroundClosure = ajc$aroundClosure; sayHello_aroundBody0(target);
      System.out.println("事务结束 ...");
    }
}
```

不难发现这个Hello.class文件不是由原来的Hello.java文件编译得到的，该Hello.class里新增了很多内容——这表明AspectJ在编译时“自动”编译得到了一个新类，这个新类增强了原有的Hello.java类的功能，因此AspectJ通常被称为编译时增强的AOP框架。

提示：与AspectJ相对的还有另外一种AOP框架，它们不需要在编译时对目标类进行增强，而是运行时生成目标类的代理类，该代理类要么与目标类实现相同的接口，要么是目标类的子类。总之，代理类的实例可作为目标类的实例来使用。一般来说，编译时增强的AOP框架在性能上更有优势，因为运行时动态增强的AOP框架需要每次运行时都进行动态增强。

实际上，AspectJ允许同时为多个方法添加新功能，只要我们定义Pointcut时指定匹配更多的方法即可。如下片段：

```java
pointcut xxxPointcut() 
     :execution(void H*.say*());
```

上面程序中的xxxPointcut将可以匹配所有以H开头的类中、所有以say开头的方法，但该方法返回的必须是void；如果不想匹配任意的返回值类型，则可将代码改为如下形式：

```java
pointcut xxxPointcut()
    :execution(* H*.say*());
```

关于如何定义AspectJ中的Aspect、Pointcut等，读者可以参考AspectJ安装路径下的doc目录里的quick5.pdf文件。

### 使用Spring AOP

与AspectJ相同的是，Spring AOP同样需要对目标类进行增强，也就是生成新的AOP代理类；与AspectJ不同的是，Spring AOP无需使用任何特殊命令对Java源代码进行编译，它采用运行时动态地、在内存中临时生成“代理类”的方式来生成AOP代理。

Spring允许使用AspectJ Annotation用于定义方面（Aspect）、切入点（Pointcut）和增强处理（Advice），Spring框架则可识别并根据这些Annotation来生成AOP代理。Spring只是使用了和AspectJ 5一样的注解，但并没有使用AspectJ的编译器或者织入器（Weaver），底层依然使用的是Spring AOP，依然是在运行时动态生成AOP代理，并不依赖于AspectJ的编译器或者织入器。

简单地说，Spring依然采用运行时生成动态代理的方式来增强目标对象，所以它不需要增加额外的编译，也不需要AspectJ的织入器支持；而AspectJ在采用编译时增强，所以AspectJ需要使用自己的编译器来编译Java文件，还需要织入器。

为了启用Spring对@AspectJ方面配置的支持，并保证Spring容器中的目标Bean被一个或多个方面自动增强，必须在Spring配置文件中配置如下片段：

```xml
<?xml version="1.0" encoding="GBK"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:aop="http://www.springframework.org/schema/aop"
    xsi:schemaLocation="http://www.springframework.org/schema/beans
    http://www.springframework.org/schema/beans/spring-beans-3.0.xsd
    http://www.springframework.org/schema/aop
    http://www.springframework.org/schema/aop/spring-aop-3.0.xsd">
    <!-- 启动 @AspectJ 支持 -->
    <aop:aspectj-autoproxy/>
</beans>
```

当然，如果我们希望完全启动Spring的“零配置”功能，则还需要启用Spring的“零配置”支持，让Spring自动搜索指定路径下Bean类。

所谓自动增强，指的是Spring会判断一个或多个方面是否需要对指定Bean进行增强，并据此自动生成相应的代理，从而使得增强处理在合适的时候被调用。

如果不打算使用Spring的XML Schema配置方式，则应该在Spring配置文件中增加如下片段来启用@AspectJ支持。

```xml
<!-- 启动 @AspectJ 支持 -->
<bean class="org.springframework.aop.aspectj.annotation.AnnotationAwareAspectJAutoProxyCreator"/>
```

上面配置文件中的AnnotationAwareAspectJAutoProxyCreator是一个Bean后处理器（BeanPostProcessor），该Bean后处理器将会为容器中Bean生成AOP代理。

当启动了@AspectJ支持后，只要我们在Spring容器中配置一个带@Aspect注释的Bean，Spring将会自动识别该Bean，并将该Bean作为方面Bean处理。

在Spring容器中配置方面Bean（即带@Aspect注释的Bean），与配置普通Bean没有任何区别，一样使用`<bean.../>`元素进行配置，一样支持使用依赖注入来配置属性值；如果我们启动了Spring的“零配置”特性，一样可以让Spring自动搜索，并装载指定路径下的方面Bean。

使用@Aspect标注一个Java类，该Java类将会作为方面Bean，如下面代码片段所示：
