---
title: 原型模式
date: 2016-08-15 11:23:16
categories: 学术
tags: Pattern
toc: true
---

孙悟空是《西游记》中的一号雄性主角，关于他（或它）拔毛变小猴的故事几乎人人皆知，孙悟空可以用猴毛根据自己的形象，复制（又称“克隆”或“拷贝”）出很多跟自己长得一模一样的“身外身”来。在设计模式中也存在一个类似的模式，可以通过一个原型对象克隆出多个一模一样的对象，该模式称之为原型模式。

### 基本定义

在使用原型模式时，我们需要首先创建一个原型对象，再通过复制这个原型对象来创建更多同类型的对象。原型模式是一种对象创建型模式。

原型模式的工作原理很简单：将一个原型对象传给那个要发动创建的对象，这个要发动创建的对象通过请求原型对象拷贝自己来实现创建过程。由于在软件系统中我们经常会遇到需要创建多个相同或者相似对象的情况，因此原型模式在真实开发中的使用频率还是非常高的。原型模式是一种“另类”的创建型模式，创建克隆对象的工厂就是原型类自身，工厂方法由克隆方法来实现。

需要注意的是通过克隆方法所创建的对象是全新的对象，它们在内存中拥有新的地址，通常对克隆所产生的对象进行修改对原型对象不会造成任何影响，每一个克隆对象都是相互独立的。通过不同的方式修改可以得到一系列相似但不完全相同的对象。

### 模式结构

原型模式的结构如图下图所示：

![原型模式](/images/design-pattern-prototype.gif "Prototype")

在原型模式结构图中包含如下几个角色：

* Prototype（抽象原型类）：它是声明克隆方法的接口，是所有具体原型类的公共父类，可以是抽象类也可以是接口，甚至还可以是具体实现类。
* ConcretePrototype（具体原型类）：它实现在抽象原型类中声明的克隆方法，在克隆方法中返回自己的一个克隆对象。
* Client（客户类）：让一个原型对象克隆自身从而创建一个新的对象，在客户类中只需要直接实例化或通过工厂方法等方式创建一个原型对象，再通过调用该对象的克隆方法即可得到多个相同的对象。由于客户类针对抽象原型类Prototype编程，因此用户可以根据需要选择具体原型类，系统具有较好的可扩展性，增加或更换具体原型类都很方便。

原型模式的核心在于如何实现克隆方法，下面将介绍两种在Java语言中常用的克隆实现方法：

#### 通用实现方法

通用的克隆实现方法是在具体原型类的克隆方法中实例化一个与自身类型相同的对象并将其返回，并将相关的参数传入新创建的对象中，保证它们的成员属性相同。示意代码如下所示：

```java
class ConcretePrototype implements Prototype {
    // 成员属性
    private String  attr;

    public void  setAttr(String attr) {
        this.attr = attr;
    }

    public String  getAttr() {
        return this.attr;
    }

    //克隆方法
    public Prototype  clone() {
        //创建新对象
        Prototype  prototype = new ConcretePrototype();
        prototype.setAttr(this.attr);
        return prototype;
    }
}
```

在客户类中我们只需要创建一个ConcretePrototype对象作为原型对象，然后调用其clone()方法即可得到对应的克隆对象，如下代码所示：

```java
Prototype obj1 = new ConcretePrototype();
obj1.setAttr("Sunny");
Prototype obj2  = obj1.clone();
```

这种方法可作为原型模式的通用实现，它与编程语言特性无关，任何面向对象语言都可以使用这种形式来实现对原型的克隆。

#### Java语言提供的clone()方法

学过Java语言的人都知道，所有的Java类都继承自java.lang.Object。事实上，Object类提供一个clone()方法，可以将一个Java对象复制一份。因此在Java中可以直接使用Object提供的clone()方法来实现对象的克隆，Java语言中的原型模式实现很简单。

需要注意的是能够实现克隆的Java类必须实现一个标识接口Cloneable，表示这个Java类支持被复制。如果一个类没有实现这个接口但是调用了clone()方法，Java编译器将抛出一个CloneNotSupportedException异常。如下代码所示：

```java
class ConcretePrototype implements  Cloneable {
    ...
    public Prototype  clone() {
    　　Object object = null;
    　　try {
    　　　　　object = super.clone();
    　　} catch (CloneNotSupportedException exception) {
    　　　　　System.err.println("Not support cloneable");
    　　}
    　　return (Prototype )object;
    }
    ...
}
```

在客户端创建原型对象和克隆对象也很简单，如下代码所示：

```java
Prototype obj1  = new ConcretePrototype();
Prototype obj2  = obj1.clone();
```

一般而言，Java语言中的clone()方法满足：

1. 对任何对象x，都有x.clone() != x，即克隆对象与原型对象不是同一个对象；
2. 对任何对象x，都有x.clone().getClass() == x.getClass()，即克隆对象与原型对象的类型一样；
3. 如果对象x的equals()方法定义恰当，那么x.clone().equals(x)应该成立。

为了获取对象的一份拷贝，我们可以直接利用Object类的clone()方法，具体步骤如下：

1. 在派生类中覆盖基类的clone()方法，并声明为public；
2. 在派生类的clone()方法中，调用super.clone()；
3. 派生类需实现Cloneable接口。

此时，Object类相当于抽象原型类，所有实现了Cloneable接口的类相当于具体原型类。

### 实现

开发人员决定使用原型模式来实现工作周报的快速创建，快速创建工作周报结构图如图所示：

![快速创建工作周报结构图](/images/design-pattern-prototype-example.gif "Prototype Example")

图中，WeeklyLog充当具体原型类，Object类充当抽象原型类，clone()方法为原型方法。WeeklyLog类的代码如下所示：

```java
/**
 * 工作周报WeeklyLog：具体原型类，考虑到代码的可读性和易理解性，只列出部分与模式相关的核心代码
 */
public class WeeklyLog implements Cloneable {
       private  String name;
       private  String date;
       private  String content;
       public  void setName(String name) {
              this.name  = name;
       }
       public  void setDate(String date) {
              this.date  = date;
       }
       public  void setContent(String content) {
              this.content  = content;
       }
       public  String getName() {
              return  (this.name);
       }
       public  String getDate() {
              return  (this.date);
       }
       public  String getContent() {
              return  (this.content);
       }
       //克隆方法clone()，此处使用Java语言提供的克隆机制
       public WeeklyLog clone() {
              Object obj = null;
              try {
                     obj = super.clone();
                     return (WeeklyLog)obj;
              } catch (CloneNotSupportedException e) {
                     System.out.println("不支持复制！");
                     return null;
              }
       }
}
```

编写如下客户端测试代码：

```java
public class Client {
       public  static void main(String args[]) {
              // 创建原型对象
              WeeklyLog log_previous = new WeeklyLog();
              log_previous.setName("张无忌");
              log_previous.setDate("第12周");
              log_previous.setContent("这周工作很忙，每天加班！");

              System.out.println("****周报****");
              System.out.println("周次：" +  log_previous.getDate());
              System.out.println("姓名：" +  log_previous.getName());
              System.out.println("内容：" +  log_previous.getContent());
              System.out.println("--------------------------------");

              WeeklyLog  log_new;
              // 调用克隆方法创建克隆对象
              log_new  = log_previous.clone();
              log_new.setDate("第13周");
              System.out.println("****周报****");
              System.out.println("周次：" + log_new.getDate());
              System.out.println("姓名：" + log_new.getName());
              System.out.println("内容：" + log_new.getContent());
       }
}
```

编译并运行程序，输出结果如下：

```bash
****周报****
周次：第12周
姓名：张无忌
内容：这周工作很忙，每天加班！
--------------------------------
****周报****
周次：第13周
姓名：张无忌
内容：这周工作很忙，每天加班！
```

通过已创建的工作周报可以快速创建新的周报，然后再根据需要修改周报，无须再从头开始创建。原型模式为工作流系统中任务单的快速生成提供了一种解决方案。

通过引入原型模式，公司OA系统支持工作周报的快速克隆，极大提高了工作周报的编写效率，受到员工的一致好评。但有员工又发现一个问题，有些工作周报带有附件，例如经理助理“小龙女”的周报通常附有本周项目进展报告汇总表、本周客户反馈信息汇总表等，如果使用上述原型模式来复制周报，周报虽然可以复制，但是周报的附件并不能复制，这是由于什么原因导致的呢？如何才能实现周报和附件的同时复制呢？我们在本节将讨论如何解决这些问题。

在回答这些问题之前，先介绍一下两种不同的克隆方法，浅克隆(ShallowClone)和深克隆(DeepClone)。在Java语言中，数据类型分为值类型（基本数据类型）和引用类型，值类型包括int、double、byte、boolean、char等简单数据类型，引用类型包括类、接口、数组等复杂类型。浅克隆和深克隆的主要区别在于是否支持引用类型的成员变量的复制，下面将对两者进行详细介绍。

#### 浅克隆

在浅克隆中，如果原型对象的成员变量是值类型，将复制一份给克隆对象；如果原型对象的成员变量是引用类型，则将引用对象的地址复制一份给克隆对象，也就是说原型对象和克隆对象的成员变量指向相同的内存地址。简单来说，在浅克隆中，当对象被复制时只复制它本身和其中包含的值类型的成员变量，而引用类型的成员对象并没有复制，如图所示：

![浅克隆示意图](/images/design-pattern-prototype-shallow-clone.gif "Shallow Clone")

在Java语言中，通过覆盖Object类的clone()方法可以实现浅克隆。为了更好地理解浅克隆和深克隆的区别，我们首先使用浅克隆来实现工作周报和附件类的复制，其结构如图所示：

![浅克隆列子](/images/design-pattern-prototype-shallow-clone-example.gif "Shallow Clone Example")

附件类Attachment代码如下：

```java
//附件类
public class Attachment {
  private  String name; //附件名
  public  void setName(String name) {
    this.name  = name;
  }
  public  String getName() {
    return  this.name;
  }
  public void download() {
    System.out.println("下载附件，文件名为" + name);
  }
}
```

修改工作周报类WeeklyLog，修改后的代码如下：

```java
/**
 * 工作周报WeeklyLog：具体原型类，考虑到代码的可读性和易理解性，只列出部分与模式相关的核心代码
 */
public class WeeklyLog implements Cloneable {
       // 为了简化设计和实现，假设一份工作周报中只有一个附件对象，实际情况中可以包含多个附件，
       // 可以通过List等集合对象来实现
       private Attachment attachment;
       private String name;
       private String date;
       private String content;
       public void setName(String name) {
              this.name  = name;
       }
       public  void setDate(String date) {
              this.date  = date;
       }
       public  void setContent(String content) {
              this.content  = content;
       }
       public void setAttachment(Attachment attachment) {
              this.attachment = attachment;
       }
       public  String getName() {
              return  (this.name);
       }
       public  String getDate() {
              return  (this.date);
       }
       public  String getContent() {
              return this.content;
       }
       public Attachment getAttachment() {
              return this.attachment;
       }
       //克隆方法clone()，此处使用Java语言提供的克隆机制
       public WeeklyLog clone() {
              Object obj = null;
              try {
                     obj = super.clone();
                     return (WeeklyLog)obj;
              } catch (CloneNotSupportedException e) {
                     System.out.println("不支持复制！");
                     return null;
              }
       }
}
```

客户端代码如下所示：

```java
public class Client {
  public  static void main(String args[]) {
    WeeklyLog  log_previous, log_new;
    log_previous  = new WeeklyLog(); //创建原型对象
    Attachment  attachment = new Attachment(); //创建附件对象
    log_previous.setAttachment(attachment);  //将附件添加到周报中
    log_new  = log_previous.clone(); //调用克隆方法创建克隆对象
    //比较周报
    System.out.println("周报是否相同？ " + (log_previous ==  log_new));
    //比较附件
    System.out.println("附件是否相同？ " +  (log_previous.getAttachment() == log_new.getAttachment()));
  }
}
```

编译并运行程序，输出结果如下：

```bash
周报是否相同？ false
附件是否相同？ true
```

由于使用的是浅克隆技术，因此工作周报对象复制成功，通过“==”比较原型对象和克隆对象的内存地址时输出false；但是比较附件对象的内存地址时输出true，说明它们在内存中是同一个对象。

#### 深克隆

在深克隆中，无论原型对象的成员变量是值类型还是引用类型，都将复制一份给克隆对象，深克隆将原型对象的所有引用对象也复制一份给克隆对象。简单来说，在深克隆中，除了对象本身被复制外，对象所包含的所有成员变量也将复制，如图所示：

![深克隆示意图](/images/design-pattern-prototype-deep-clone.gif "Deep Clone")

在Java语言中，如果需要实现深克隆，可以通过序列化(Serialization)等方式来实现。序列化就是将对象写到流的过程，写到流中的对象是原有对象的一个拷贝，而原对象仍然存在于内存中。通过序列化实现的拷贝不仅可以复制对象本身，而且可以复制其引用的成员对象，因此通过序列化将对象写到一个流中，再从流里将其读出来，可以实现深克隆。需要注意的是能够实现序列化的对象其类必须实现Serializable接口，否则无法实现序列化操作。下面我们使用深克隆技术来实现工作周报和附件对象的复制，由于要将附件对象和工作周报对象都写入流中，因此两个类均需要实现Serializable接口，其结构如图所示：

![深克隆例子](/images/design-pattern-prototype-deep-clone-example.gif "Deep Clone Example")

修改后的附件类Attachment代码如下：

```java
import java.io.*;

//附件类
public class Attachment implements Serializable {
  private  String name; //附件名
  public  void setName(String name) {
    this.name  = name;
  }
  public  String getName() {
    return  this.name;
  }
  public void download() {
    System.out.println("下载附件，文件名为" + name);
  }
}
```

工作周报类WeeklyLog不再使用Java自带的克隆机制，而是通过序列化来从头实现对象的深克隆，我们需要重新编写clone()方法，修改后的代码如下：

```java
import java.io.*;

/**
 * 工作周报WeeklyLog：具体原型类，考虑到代码的可读性和易理解性，只列出部分与模式相关的核心代码
 */
public class WeeklyLog implements Serializable {
       // 为了简化设计和实现，假设一份工作周报中只有一个附件对象，实际情况中可以包含多个附件，
       // 可以通过List等集合对象来实现
       private Attachment attachment;
       private String name;
       private String date;
       private String content;
       public void setName(String name) {
              this.name  = name;
       }
       public  void setDate(String date) {
              this.date  = date;
       }
       public  void setContent(String content) {
              this.content  = content;
       }
       public void setAttachment(Attachment attachment) {
              this.attachment = attachment;
       }
       public  String getName() {
              return  (this.name);
       }
       public  String getDate() {
              return  (this.date);
       }
       public  String getContent() {
              return this.content;
       }
       public Attachment getAttachment() {
              return this.attachment;
       }
       //使用序列化技术实现深克隆
       public WeeklyLog deepClone() throws IOException, ClassNotFoundException, OptionalDataException {
              //将对象写入流中
              ByteArrayOutputStream bao = new  ByteArrayOutputStream();
              ObjectOutputStream oos = new  ObjectOutputStream(bao);
              oos.writeObject(this);

              //将对象从流中取出
              ByteArrayInputStream bis = new  ByteArrayInputStream(bao.toByteArray());
              ObjectInputStream ois = new  ObjectInputStream(bis);
              return  (WeeklyLog)ois.readObject();
       }
}
```

客户端代码如下所示：

```java
public class Client {
       public  static void main(String args[]) {
              WeeklyLog  log_previous, log_new = null;
              log_previous  = new WeeklyLog(); //创建原型对象
              Attachment  attachment = new Attachment(); //创建附件对象
              log_previous.setAttachment(attachment);  //将附件添加到周报中
              try {
                     log_new =  log_previous.deepClone(); //调用深克隆方法创建克隆对象
              } catch (Exception e) {
                     System.err.println("克隆失败！");
              }
              //比较周报
              System.out.println("周报是否相同？ " + (log_previous ==  log_new));
              //比较附件
              System.out.println("附件是否相同？ " +  (log_previous.getAttachment() == log_new.getAttachment()));
       }
}
```

编译并运行程序，输出结果如下：

```bash
周报是否相同？  false
附件是否相同？  false
```

从输出结果可以看出，由于使用了深克隆技术，附件对象也得以复制，因此用“==”比较原型对象的附件和克隆对象的附件时输出结果均为false。深克隆技术实现了原型对象和克隆对象的完全独立，对任意克隆对象的修改都不会给其他对象产生影响，是一种更为理想的克隆实现方式。

#### 原型管理器

原型管理器(Prototype Manager)是将多个原型对象存储在一个集合中供客户端使用，它是一个专门负责克隆对象的工厂，其中定义了一个集合用于存储原型对象，如果需要某个原型对象的一个克隆，可以通过复制集合中对应的原型对象来获得。在原型管理器中针对抽象原型类进行编程，以便扩展。其结构如图所示：

![带原型管理器的原型模式](/images/design-pattern-prototype-manager.gif "Prototype Manager")

下面通过模拟一个简单的公文管理器来介绍原型管理器的设计与实现：

某软件公司在日常办公中有许多公文需要创建、递交和审批，例如《可行性分析报告》、《立项建议书》、《软件需求规格说明书》、《项目进展报告》等，为了提高工作效率，在OA系统中为各类公文均创建了模板，用户可以通过这些模板快速创建新的公文，这些公文模板需要统一进行管理，系统根据用户请求的不同生成不同的新公文。

我们使用带原型管理器的原型模式实现公文管理器的设计，其结构如下图所示：

![公文管理器结构图](/images/design-pattern-prototype-manager-example.gif "Prototype Manager Example")

以下是实现该功能的一些核心代码，考虑到代码的可读性，我们对所有的类都进行了简化：

```java
import java.util.*;

//抽象公文接口，也可定义为抽象类，提供clone()方法的实现，将业务方法声明为抽象方法
interface OfficialDocument extends  Cloneable {
  public  OfficialDocument clone();
  public  void display();
}

//可行性分析报告(Feasibility Analysis Report)类
class FAR implements OfficialDocument {
  public  OfficialDocument clone() {
    OfficialDocument  far = null;
    try {
      far  = (OfficialDocument)super.clone();
    } catch (CloneNotSupportedException  e) {
      System.out.println("不支持复制！");
    }
    return  far;
  }

  public  void display() {
    System.out.println("《可行性分析报告》");
  }
}

//软件需求规格说明书(Software Requirements Specification)类
class SRS implements OfficialDocument {
  public  OfficialDocument clone() {
    OfficialDocument  srs = null;
    try {
      srs  = (OfficialDocument)super.clone();
    } catch (CloneNotSupportedException  e) {
      System.out.println("不支持复制！");
    }
    return  srs;
  }

  public  void display() {
    System.out.println("《软件需求规格说明书》");
  }
}

//原型管理器（使用饿汉式单例实现）
public class PrototypeManager {
  //定义一个Hashtable，用于存储原型对象
  private Hashtable ht = new Hashtable();
  private static PrototypeManager pm =  new PrototypeManager();

  //为Hashtable增加公文对象
  private  PrototypeManager() {
    ht.put("far", new  FAR());
    ht.put("srs", new  SRS());
  }

  //增加新的公文对象
  public void addOfficialDocument(String  key, OfficialDocument doc) {
    ht.put(key, doc);
  }

  //通过浅克隆获取新的公文对象
  public OfficialDocument  getOfficialDocument(String key) {
    return  ((OfficialDocument)ht.get(key)).clone();
  }

  public static PrototypeManager  getPrototypeManager() {
    return pm;
  }
}
```

客户端代码如下所示：

```java
public class Client {
       public  static void main(String args[]) {
              //获取原型管理器对象
              PrototypeManager pm =  PrototypeManager.getPrototypeManager();

              OfficialDocument  doc1, doc2, doc3, doc4;

              doc1  = pm.getOfficialDocument("far");
              doc1.display();
              doc2  = pm.getOfficialDocument("far");
              doc2.display();
              System.out.println(doc1  == doc2);

              doc3  = pm.getOfficialDocument("srs");
              doc3.display();
              doc4  = pm.getOfficialDocument("srs");
              doc4.display();
              System.out.println(doc3  == doc4);
       }
}
```

编译并运行程序，输出结果如下：

```bash
《可行性分析报告》
《可行性分析报告》
false
《软件需求规格说明书》
《软件需求规格说明书》
false
```

在PrototypeManager中定义了一个Hashtable类型的集合对象，使用“键值对”来存储原型对象，客户端可以通过Key（如“far”或“srs”）来获取对应原型对象的克隆对象。PrototypeManager类提供了类似工厂方法的getOfficialDocument()方法用于返回一个克隆对象。在本实例代码中，我们将PrototypeManager设计为单例类，使用饿汉式单例实现，确保系统中有且仅有一个PrototypeManager对象，有利于节省系统资源，并可以更好地对原型管理器对象进行控制。

### 总结

原型模式作为一种快速创建大量相同或相似对象的方式，在软件开发中应用较为广泛，很多软件提供的复制(Ctrl + C)和粘贴(Ctrl + V)操作就是原型模式的典型应用，下面对该模式的使用效果和适用情况进行简单的总结。

#### 优点

原型模式的主要优点如下：
1. 当创建新的对象实例较为复杂时，使用原型模式可以简化对象的创建过程，通过复制一个已有实例可以提高新实例的创建效率。
2. 扩展性较好，由于在原型模式中提供了抽象原型类，在客户端可以针对抽象原型类进行编程，而将具体原型类写在配置文件中，增加或减少产品类对原有系统都没有任何影响。
3. 原型模式提供了简化的创建结构，工厂方法模式常常需要有一个与产品类等级结构相同的工厂等级结构，而原型模式就不需要这样，原型模式中产品的复制是通过封装在原型类中的克隆方法实现的，无须专门的工厂类来创建产品。
4. 可以使用深克隆的方式保存对象的状态，使用原型模式将对象复制一份并将其状态保存起来，以便在需要的时候使用（如恢复到某一历史状态），可辅助实现撤销操作。

#### 缺点

原型模式的主要缺点如下：
1. 需要为每一个类配备一个克隆方法，而且该克隆方法位于一个类的内部，当对已有的类进行改造时，需要修改源代码，违背了“开闭原则”。
2. 在实现深克隆时需要编写较为复杂的代码，而且当对象之间存在多重的嵌套引用时，为了实现深克隆，每一层对象对应的类都必须支持深克隆，实现起来可能会比较麻烦。

#### 适用场景

在以下情况下可以考虑使用原型模式：

1. 创建新对象成本较大（如初始化需要占用较长的时间，占用太多的CPU资源或网络资源），新的对象可以通过原型模式对已有对象进行复制来获得，如果是相似对象，则可以对其成员变量稍作修改。
2. 如果系统要保存对象的状态，而对象的状态变化很小，或者对象本身占用内存较少时，可以使用原型模式配合备忘录模式来实现。
3. 需要避免使用分层次的工厂类来创建分层次的对象，并且类的实例对象只有一个或很少的几个组合状态，通过复制原型对象得到新实例可能比使用构造函数创建一个新实例更加方便。
