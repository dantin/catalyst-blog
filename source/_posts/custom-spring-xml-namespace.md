title: 自定义Spring XML Bean配置
date: 2016-05-31 22:10:47
categories: 工程
tags: [Spring]
toc: true
---

在很多情况下，我们需要为框架提供可配置支持，简单的做法可以直接基于Spring的标准Bean来配置，但配置较为复杂或者需要更多丰富控制的时候，会显得非常笨拙。Spring提供了可扩展Schema的支持，允许我们自定义Spring XML Bean的配置。

本文简单记录这一技术的使用方法。

### 传统XML方式

传统Spring XML方式的Bean定义语法。

```xml
<bean id="..." class="...">
    <property name="xxx", value="" />
</bean>
```

__TIPS__: Spring 2.0之前使用的是DTD做XML校验，2.0之后开始使用XSD文件。

使用DTD需要在XML开头指定DTD文件的位置：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE beans PUBLIC "-//SPRING//DTD BEAN 2.0//EN"
        "http://www.springframework.org/dtd/spring-beans-2.0.dtd">

<beans>

<!-- bean definitions here -->

</beans>
```

使用XML Schema-style则是：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="
        http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">

    <!-- bean definitions here -->

</beans>
```
### Customize方式

自定义方式允许我们定义自己独有的标签，比如Dubbo框架，就是自定义一套标签，方便用户定义和引用RPC服务：

```xml
<!-- Export remote service: -->
<dubbo:service interface="com.foo.BarService" ref="barService" />
<!-- Refer remote service: -->
<dubbo:reference id="barService" interface="com.foo.BarService" />
```

上面的`<dubbo:service>`和`<dubbo:reference>`是Dubbo框架自定义的标签，Spring本身是不支持的，但是当我们使用这个标签定义Bean之后，却能引用到这些Bean。

### 实现原理

Spring在设计的时候就已经考虑到这点了，所以只要准许它的规范就可以很容易的实现自定义标签的：

> Creating new XML configuration extensions can be done by following these (relatively) simple steps:
> 
> 1. Authoring an XML schema to describe your custom element(s).
> 2. Coding a custom NamespaceHandler implementation (this is an easy step, don’t worry).
> 3. Coding one or more BeanDefinitionParser implementations (this is where the real work is done).
> 4. Registering the above artifacts with Spring (this too is an easy step).

### 实现步骤

Spring官方文档有一个简单的例子：

假如要定义一个SimpleDateFormat对象，通常的定义方式是：

```xml
<bean id="dateFormat" class="java.text.SimpleDateFormat">
    <constructor-arg value="yyyy-HH-dd HH:mm"/>
    <property name="lenient" value="true"/>
</bean>
```

现在我们要通过一种更友好简单的方式定义，比如下面：

```xml
<halo:dateformat id="test"
    pattern="yyyy-MM-dd" 
    lenient="true"/>
```

#### Authoring the schema

指定验证XML语法的XSD文件：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xsd:schema xmlns="http://www.cosmos.com/schema/halo"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema"
            xmlns:beans="http://www.springframework.org/schema/beans"
            targetNamespace="http://www.cosmos.com/schema/halo"
            elementFormDefault="qualified"
            attributeFormDefault="unqualified">

    <xsd:import namespace="http://www.springframework.org/schema/beans"/>

    <xsd:element name="dateformat">
        <xsd:complexType>
            <xsd:complexContent>
                <xsd:extension base="beans:identifiedType">
                    <xsd:attribute name="lenient" type="xsd:boolean"/>
                    <xsd:attribute name="pattern" type="xsd:string" use="required"/>
                </xsd:extension>
            </xsd:complexContent>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
```

#### Coding a NamespaceHandler

上面的XSD文件仅仅是验证XML配置语法的正确性，但是要让这个配置真的起作用（达到创建一个SimpleDateFormat的效果），那么还需要定义一个NamespaceHandler用于解析这段配置。

NamespaceHandler是一个非常简单的接口，只有四个接口：

```java
package org.springframework.beans.factory.xml;

import org.w3c.dom.Element;
import org.w3c.dom.Node;

import org.springframework.beans.factory.config.BeanDefinition;
import org.springframework.beans.factory.config.BeanDefinitionHolder;

/**
 * Base interface used by the {@link DefaultBeanDefinitionDocumentReader}
 * for handling custom namespaces in a Spring XML configuration file.
 *
 * <p>Implementations are expected to return implementations of the
 * {@link BeanDefinitionParser} interface for custom top-level tags and
 * implementations of the {@link BeanDefinitionDecorator} interface for
 * custom nested tags.
 *
 * <p>The parser will call {@link #parse} when it encounters a custom tag
 * directly under the {@code &lt;beans&gt;} tags and {@link #decorate} when
 * it encounters a custom tag directly under a {@code &lt;bean&gt;} tag.
 *
 * <p>Developers writing their own custom element extensions typically will
 * not implement this interface drectly, but rather make use of the provided
 * {@link NamespaceHandlerSupport} class.
 *
 * @since 2.0
 * @see DefaultBeanDefinitionDocumentReader
 * @see NamespaceHandlerResolver
 */
public interface NamespaceHandler {

    /**
     * Invoked by the {@link DefaultBeanDefinitionDocumentReader} after
     * construction but before any custom elements are parsed.
     * @see NamespaceHandlerSupport#registerBeanDefinitionParser(String, BeanDefinitionParser)
     */
    void init();

    /**
     * Parse the specified {@link Element} and register any resulting
     * {@link BeanDefinition BeanDefinitions} with the
     * {@link org.springframework.beans.factory.support.BeanDefinitionRegistry}
     * that is embedded in the supplied {@link ParserContext}.
     * <p>Implementations should return the primary {@code BeanDefinition}
     * that results from the parse phase if they wish to be used nested
     * inside (for example) a {@code &lt;property&gt;} tag.
     * <p>Implementations may return {@code null} if they will
     * <strong>not</strong> be used in a nested scenario.
     * @param element the element that is to be parsed into one or more {@code BeanDefinitions}
     * @param parserContext the object encapsulating the current state of the parsing process
     * @return the primary {@code BeanDefinition} (can be {@code null} as explained above)
     */
    BeanDefinition parse(Element element, ParserContext parserContext);

    /**
     * Parse the specified {@link Node} and decorate the supplied
     * {@link BeanDefinitionHolder}, returning the decorated definition.
     * <p>The {@link Node} may be either an {@link org.w3c.dom.Attr} or an
     * {@link Element}, depending on whether a custom attribute or element
     * is being parsed.
     * <p>Implementations may choose to return a completely new definition,
     * which will replace the original definition in the resulting
     * {@link org.springframework.beans.factory.BeanFactory}.
     * <p>The supplied {@link ParserContext} can be used to register any
     * additional beans needed to support the main definition.
     * @param source the source element or attribute that is to be parsed
     * @param definition the current bean definition
     * @param parserContext the object encapsulating the current state of the parsing process
     * @return the decorated definition (to be registered in the BeanFactory),
     * or simply the original bean definition if no decoration is required.
     * A {@code null} value is strictly speaking invalid, but will be leniently
     * treated like the case where the original bean definition gets returned.
     */
    BeanDefinitionHolder decorate(Node source, BeanDefinitionHolder definition, ParserContext parserContext);

}
```

但是一般不直接使用，而是使用NamespaceHandlerSupport。这个类允许我们注册Parser和Decorator来解析特定的XML元素。

```java
package com.cosmos.halo.config.springsupport;

import org.springframework.beans.factory.xml.NamespaceHandlerSupport;

public class HaloNamespaceHandler extends NamespaceHandlerSupport {

    @Override
    public void init() {
        registerBeanDefinitionParser("dateformat", new SimpleDateFormatBeanDefinitionParser());
    }
}
```

#### 定义相应的BeanDefinitionParser

BeanDefinitionParser的职责是将一个唯一的定级XML元素解析为对应的BeanDefinition。

```java
package com.cosmos.halo.config.springsupport;

import org.springframework.beans.factory.support.BeanDefinitionBuilder;
import org.springframework.beans.factory.xml.AbstractSingleBeanDefinitionParser;
import org.springframework.util.StringUtils;
import org.w3c.dom.Element;

import java.text.SimpleDateFormat;

public class SimpleDateFormatBeanDefinitionParser extends AbstractSingleBeanDefinitionParser {

    protected Class getBeanClass(Element element) {
        return SimpleDateFormat.class;
    }

    protected void doParse(Element element, BeanDefinitionBuilder bean) {
        // this will never be null since the schema explicitly requires that a value be supplied
        String pattern = element.getAttribute("pattern");
        bean.addConstructorArgValue(pattern);

        // this however is an optional property
        String lenient = element.getAttribute("lenient");
        if (StringUtils.hasText(lenient)) {
            bean.addPropertyValue("lenient", Boolean.valueOf(lenient));
        }
    }
}

```

同样，有很多基础的工作都在基类中做掉了，只需要重载几个重要的方法，就可以了。

#### Registering the handler and the schema

最后我们要让Spring在加载XML配置文件的时候能够去加载我们的NamespaceHandler类和XSD schema文件。这是通过两个配置文件告诉Spring的：

##### META-INF/spring.handlers

```text
http\://www.cosmos.com/schema/halo=com.cosmos.halo.config.springsupport.HaloNamespaceHandler
```
__NOTE__因为`:`是一个合法的java properties文件格式，所以这里要转义一下。

##### META-INF/spring.schemas

```text
http\://www.cosmos.com/schema/halo.xsd=META-INF/halo.xsd
```

### 测试

准备applicationContext.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:halo="http://www.cosmos.com/schema/halo"
       xsi:schemaLocation="
       http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-4.2.xsd
       http://www.cosmos.com/schema/halo http://www.cosmos.com/schema/halo.xsd">
    <halo:dateformat id="test" pattern="yyyy-MM-dd" lenient="true"/>
</beans>
```

编写Java类。

```java
package com.cosmos.halo.config.springsupport;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

import java.text.SimpleDateFormat;
import java.util.Date;

public class HaloTagTest {

    public static void main(String[] args) {
        ApplicationContext ctx = new ClassPathXmlApplicationContext("classpath:/application.xml");
        SimpleDateFormat p = (SimpleDateFormat)ctx.getBean("test");
        System.out.println(p.format(new Date()));
    }
}
```

输出

```shell
2016-05-31
```

### 使用xbean-spring实现自定义标签

这种方式还是需要使用最原始的org.w3c.dom.Element解析XML元素，能不能直接将配置文件注入到一个POJO对象中呢？[xbean-spring](http://svn.apache.org/repos/asf/geronimo/xbean/trunk/xbean-spring/)项目就是为了解决这个问题的。

它会把XML元素映射成你定义的POJO类（使用@XBean注解），这点非常类似于JAXB或者XStream。然后使用maven插件将其转化为上面Spring的handler和schema机制。

这里有个例子: [xbean-spring-example](https://github.com/christian-posta/xbean-spring-example)。相应的博客在：[Easier way to create custom Spring Config Namespaces using xbean-spring](http://blog.christianposta.com/activemq/easier-way-to-create-custom-spring-config-namespaces-using-xbean-spring/)。

官方文档也有相应的说明：[custom-xml](http://geronimo.apache.org/xbean/custom-xml.html)

参考

[34. XML Schema-based configuration](http://docs.spring.io/spring/docs/current/spring-framework-reference/html/xsd-config.html)
[35. Extensible XML authoring](http://docs.spring.io/spring/docs/current/spring-framework-reference/html/extensible-xml.html)
[Creating a Custom Spring 3 XML Namespace](http://java.dzone.com/articles/creating-custom-spring-3-xml) 一个相对比较复杂的例子
[Easier way to create custom Spring Config Namespaces using xbean-spring](http://blog.christianposta.com/activemq/easier-way-to-create-custom-spring-config-namespaces-using-xbean-spring/)