---
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

```java
// 使用 @Aspect 定义一个方面类
@Aspect
public class LogAspect {
    // 定义该类的其他内容
    ...
}
```

方面类（用@Aspect修饰的类）和其他类一样可以有方法、属性定义，还可能包括切入点、增强处理定义。

当我们使用@Aspect来修饰一个Java类之后，Spring将不会把该Bean当成组件Bean处理，因此负责自动增强的后处理Bean将会略过该Bean，不会对该Bean进行任何增强处理。

开发时无须担心使用@Aspect定义的方面类被增强处理，当Spring容器检测到某个Bean类使用了@Aspect标注之后，Spring容器不会对该Bean类进行增强。

下面将会考虑采用Spring AOP来改写前面介绍的例子：

下面例子使用一个简单的Chinese类来模拟业务逻辑组件：

```java
import org.springframework.stereotype.Component;

@Component
public class Chinese {

    // 实现 Person 接口的 sayHello() 方法
    public String sayHello(String name) {
        System.out.println("-- 正在执行 sayHello 方法 --");
        // 返回简单的字符串
        return name + " Hello , Spring AOP";
    }

    // 定义一个 eat() 方法
    public void eat(String food) {
        System.out.println("我正在吃 :" + food);
    }
}
```

提供了上面Chinese类之后，接下来假设同样需要为上面Chinese类的每个方法增加事务控制、日志记录，此时可以考虑使用Around、AfterReturning两种增强处理。

先看AfterReturning增强处理代码。

```java
import org.aspectj.lang.annotation.AfterReturning;
import org.aspectj.lang.annotation.Aspect;

@Aspect
public class AfterReturningAdviceTest {

    // 匹配 com.cosmos.aop 包下所有类的、
    // 所有方法的执行作为切入点
    @AfterReturning(returning = "rvt",
            pointcut = "execution(* com.cosmos.aop.*.*(..))")
    public void log(Object rvt) {
        System.out.println("获取目标方法返回值 :" + rvt);
        System.out.println("模拟记录日志功能 ...");
    }
}
```

上面Aspect类使用了@com.cosmos.aop包下的所有类的所有方法之后织入log(Object rvt)方法。

再看Around增强处理代码：

```java
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;

@Aspect
public class AroundAdviceTest {
    // 匹配 com.cosmos.aop 包下所有类的、
    // 所有方法的执行作为切入点
    @Around("execution(* com.cosmos.aop.*.*(..))")
    public Object processTx(ProceedingJoinPoint jp)
            throws java.lang.Throwable {
        System.out.println("执行目标方法之前，模拟开始事务 ...");
        // 执行目标方法，并保存目标方法执行后的返回值
        Object rvt = jp.proceed(new String[]{"被改变的参数"});
        System.out.println("执行目标方法之后，模拟结束事务 ...");
        return rvt + " 新增的内容";
    }
}
```

与前面的AfterReturning增强处理类似的，此处同样使用了@Aspect来修饰前面Bean，其中粗体字代码指定在调用com.cosmos.aop包下的所有类的所有方法的“前后（Around）”织入processTx(ProceedingJoinPoint jp)方法。

需要指出的是，虽然此处只介绍了Spring AOP的AfterReturning、Around两种增强处理，但实际上Spring还支持Before、After、AfterThrowing等增强处理，关于Spring AOP编程更多、更细致的编程细节，可以参考《轻量级Java EE企业应用实战》一书。

本示例采用了Spring的零配置来开启Spring AOP，因此上面Chinese类使用了@Component修饰，而方面Bean则使用了@Aspect修饰，方面Bean中的Advice则分别使用了@AfterReturning、@Around修饰。接下来只要为Spring提供如下配置文件即可：

```xml
<?xml version="1.0" encoding="GBK"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:aop="http://www.springframework.org/schema/aop"
       xsi:schemaLocation="http://www.springframework.org/schema/beans 
 http://www.springframework.org/schema/beans/spring-beans-3.0.xsd 
 http://www.springframework.org/schema/context 
 http://www.springframework.org/schema/context/spring-context-3.0.xsd 
 http://www.springframework.org/schema/aop 
 http://www.springframework.org/schema/aop/spring-aop-3.0.xsd">
    <!-- 指定自动搜索 Bean 组件、自动搜索方面类 -->
    <context:component-scan base-package="com.cosmos.aop">
        <context:include-filter type="annotation"
                                expression="org.aspectj.lang.annotation.Aspect"/>
    </context:component-scan>
    <!-- 启动 @AspectJ 支持 -->
    <aop:aspectj-autoproxy/>
</beans>
```

接下来按传统方式来获取Spring容器中chinese Bean、并调用该Bean的两个方法，程序代码如下：

```java
import com.cosmos.aop.Chinese;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class BeanTest {
    public static void main(String[] args) {
        // 创建 Spring 容器
        ApplicationContext ctx = new
                ClassPathXmlApplicationContext("beans.xml");
        Chinese p = ctx.getBean("chinese", Chinese.class);
        System.out.println(p.sayHello("张三"));
        p.eat("西瓜");
    }
}
```

从上面开发过程可以看出，对于Spring AOP而言，开发者提供的业务组件、方面Bean并没有任何特别的地方。只是方面Bean需要使用@Aspect修饰即可。程序不需要使用特别的编译器、织入器进行处理。

运行上面程序，将可以看到如下执行结果：

```bash
执行目标方法之前，模拟开始事务 ...
-- 正在执行 sayHello 方法 --
执行目标方法之后，模拟结束事务 ...
获取目标方法返回值 :被改变的参数 Hello , Spring AOP 新增的内容
模拟记录日志功能 ...

被改变的参数 Hello , Spring AOP 新增的内容

执行目标方法之前，模拟开始事务 ...
我正在吃 :被改变的参数
执行目标方法之后，模拟结束事务 ...
获取目标方法返回值 :null 新增的内容
模拟记录日志功能 ...
```

虽然程序是在调用Chinese对象的sayHello、eat两个方法，但从上面运行结果不难看出：实际执行的绝对不是Chinese对象的方法，而是AOP代理的方法。也就是说，Spring AOP同样为Chinese类生成了AOP代理类。这一点可通过在程序中增加如下代码看出：

```java
System.out.println(p.getClass());
```

上面代码可以输出p变量所引用对象的实现类，再次执行程序将可以看到上面代码产生class com.cosmos.aop.Chinese$$EnhancerByCGLIB$$290441d2的输出，这才是p变量所引用的对象的实现类，这个类也就是Spring AOP动态生成的AOP代理类。从AOP代理类的类名可以看出，AOP代理类是由CGLIB来生成的。

如果将上面程序程序稍作修改：只要让上面业务逻辑类Chinese类实现一个任意接口。这种做法更符合Spring所倡导的“面向接口编程”的原则。假设程序为Chinese类提供如下Person接口，并让Chinese类实现该接口：

```java
public interface Person {
    String sayHello(String name);
    void eat(String food);
}
```

接下来让BeanTest类面向Person接口、而不是Chinese类编程。即将BeanTest类改为如下形式：

```java
import com.cosmos.aop.Person;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class BeanTest {
    public static void main(String[] args) {
        // 创建 Spring 容器
        ApplicationContext ctx = new
                ClassPathXmlApplicationContext("beans.xml");
        Person p = ctx.getBean("chinese", Person.class);
        System.out.println(p.sayHello("张三"));
        p.eat("西瓜");
        System.out.println(p.getClass());
    }
}
```

原来的程序是将面向Chinese类编程，现在将该程序改为面向Person接口编程，再次运行该程序，程序运行结果没有发生改变。只是System.out.println(p.getClass());将会输出class$Proxy7，这说明此时的AOP代理并不是由CGLIB生成的，而是由JDK动态代理生成的。

Spring AOP框架对AOP代理类的处理原则是：
* 如果目标对象的实现类实现了接口，Spring AOP将会采用JDK动态代理来生成AOP代理类；
* 如果目标对象的实现类没有实现接口，Spring AOP将会采用CGLIB来生成AOP代理类

不过这个选择过程对开发者完全透明、开发者也无需关心。

Spring AOP会动态选择使用JDK动态代理、CGLIB来生成AOP代理，如果目标类实现了接口，Spring AOP则无需CGLIB的支持，直接使用JDK提供的Proxy和InvocationHandler来生成AOP代理即可。关于如何Proxy和InvocationHandler来生成动态代理不在本文介绍范围之内，如果读者对Proxy和InvocationHandler的用法感兴趣则可自行参考Java API文档或《疯狂 Java 讲义》。

### Spring AOP原理剖析

通过前面介绍可以知道：AOP代理其实是由AOP框架动态生成的一个对象，该对象可作为目标对象使用。AOP代理包含了目标对象的全部方法，但AOP代理中的方法与目标对象的方法存在差异：AOP方法在特定切入点添加了增强处理，并回调了目标对象的方法。

AOP代理所包含的方法与目标对象的方法示意图如图3所示。

![AOP 代理的方法与目标对象的方法](/images/spring-aop-003.gif "Spring-aop-003")

Spring的AOP代理由Spring的IoC容器负责生成、管理，其依赖关系也由IoC容器负责管理。因此，AOP代理可以直接使用容器中的其他Bean实例作为目标，这种关系可由IoC容器的依赖注入提供。

纵观AOP编程，其中需要程序员参与的只有3个部分：

* 定义普通业务组件。
* 定义切入点，一个切入点可能横切多个业务组件。
* 定义增强处理，增强处理就是在AOP框架为普通业务组件织入的处理动作。

上面3个部分的第一个部分是最平常不过的事情，无须额外说明。那么进行AOP编程的关键就是定义切入点和定义增强处理。一旦定义了合适的切入点和增强处理，AOP框架将会自动生成AOP代理，而AOP代理的方法大致有如下公式：

> 代理对象的方法 = 增强处理 + 被代理对象的方法

在上面这个业务定义中，不难发现Spring AOP的实现原理其实很简单：AOP框架负责动态地生成AOP代理类，这个代理类的方法则由Advice和回调目标对象的方法所组成。

对于前面提到的图2所示的软件调用结构：当方法1、方法2、方法3……都需要去调用某个具有“横切”性质的方法时，传统的做法是程序员去手动修改方法1、方法2、方法3……、通过代码来调用这个具有“横切”性质的方法，但这种做法的可扩展性不好，因为每次都要改代码。

于是AOP框架出现了，AOP框架则可以“动态的”生成一个新的代理类，而这个代理类所包含的方法1、方法2、方法3……也增加了调用这个具有“横切”性质的方法，但这种调用由AOP框架自动生成的代理类来负责，因此具有了极好的扩展性。程序员无需手动修改方法1、方法2、方法3的代码，程序员只要定义切入点即可。AOP框架所生成的AOP代理类中包含了新的方法1、访法2、方法3，而AOP框架会根据切入点来决定是否要在方法1、方法2、方法3中回调具有“横切”性质的方法。

简而言之：AOP原理的奥妙就在于动态地生成了代理类，这个代理类实现了图2的调用，这种调用无需程序员修改代码。接下来介绍的CGLIB就是一个代理生成库，下面介绍如何使用CGLIB来生成代理类。

### 使用CGLIB生成代理类

CGLIB（Code Generation Library），简单来说，就是一个代码生成类库。它可以在运行时候动态是生成某个类的子类。

此处使用前面定义的Chinese类，现在改为直接使用CGLIB来生成代理，这个代理类同样可以实现Spring AOP代理所达到的效果。

下面先为CGLIB提供一个拦截器实现类：

```java
import org.springframework.cglib.proxy.MethodInterceptor;
import org.springframework.cglib.proxy.MethodProxy;

import java.lang.reflect.Method;

public class AroundAdvice implements MethodInterceptor {

    @Override
    public Object intercept(Object target, Method method
            , Object[] args, MethodProxy proxy) throws Throwable {
        System.out.println("执行目标方法之前，模拟开始事务 ...");
        // 执行目标方法，并保存目标方法执行后的返回值
        Object rvt = proxy.invokeSuper(target, new String[]{"被改变的参数"});
        System.out.println("执行目标方法之后，模拟结束事务 ...");
        return rvt + " 新增的内容";
    }
}
```

上面这个AroundAdvice.java的作用就像前面介绍的Around Advice，它可以在调用目标方法之前、调用目标方法之后织入增强处理。

接下来程序提供一个ChineseProxyFactory类，这个ChineseProxyFactory类会通过CGLIB来为Chinese生成代理类：

```java
import com.cosmos.aop.Chinese;
import org.springframework.cglib.proxy.Enhancer;

public class ChineseProxyFactory {

    public static Chinese getAuthInstance() {
        Enhancer en = new Enhancer();
        // 设置要代理的目标类
        en.setSuperclass(Chinese.class);
        // 设置要代理的拦截器
        en.setCallback(new AroundAdvice());
        // 生成代理类的实例
        return (Chinese) en.create();
    }
}
```

上面粗体字代码就是使用CGLIB的Enhancer生成代理对象的关键代码，此时的Enhancer将以Chinese类作为目标类，以AroundAdvice对象作为“Advice”，程序将会生成一个Chinese的子类，这个子类就是CGLIB生成代理类，它可作为Chinese对象使用，但它增强了Chinese类的方法。

测试Chinese代理类的主程序如下：

```java
import com.cosmos.aop.Chinese;
import com.cosmos.cglib.ChineseProxyFactory;

public class Main {
    public static void main(String[] args) {
        Chinese chin = ChineseProxyFactory.getAuthInstance();
        System.out.println(chin.sayHello("孙悟空"));
        chin.eat("西瓜");
        System.out.println(chin.getClass());
    }
}
```

运行上面主程序，看到如下输出结果：

```bash
执行目标方法之前，模拟开始事务 ...
-- 正在执行 sayHello 方法 --
执行目标方法之后，模拟结束事务 ...

被改变的参数 Hello , Spring AOP 新增的内容

执行目标方法之前，模拟开始事务 ...
我正在吃 :被改变的参数
执行目标方法之后，模拟结束事务 ...

class com.cosmos.aop.Chinese$$EnhancerByCGLIB$$5f88b1ad
```

从上面输出结果来看，CGLIB生成的代理完全可以作为Chinese对象来使用，而且CGLIB代理对象的sayHello()、eat()两个方法已经增加了事务控制（只是模拟），这个CGLIB代理其实就是Spring AOP所生成的AOP代理。

通过程序最后的输出，不难发现这个代理对象的实现类是com.cosmos.aop.Chinese$$EnhancerByCGLIB$$5f88b1ad，这就是CGLIB所生成的代理类，这个代理类的格式与前面Spring AOP所生成的代理类的格式完全相同。

这就是Spring AOP的根本所在：Spring AOP就是通过CGLIB来动态地生成代理对象，这个代理对象就是所谓的AOP代理，而AOP代理的方法则通过在目标对象的切入点动态地织入增强处理，从而完成了对目标方法的增强。

### 小结

AOP广泛应用于处理一些具有横切性质的系统级服务，AOP的出现是对OOP的良好补充，它使得开发者能用更优雅的方式处理具有横切性质的服务。不管是那种AOP实现，不论是AspectJ、还是Spring AOP，它们都需要动态地生成一个AOP代理类，区别只是生成AOP代理类的时机不同：AspectJ采用编译时生成AOP代理类，因此具有更好的性能，但需要使用特定的编译器进行处理；而Spring AOP则采用运行时生成AOP代理类，因此无需使用特定编译器进行处理。由于Spring AOP需要在每次运行时生成AOP代理，因此性能略差一些。

参考

[IBM developerWorkers](https://www.ibm.com/developerworks/cn/java/j-lo-springaopcglib/)
