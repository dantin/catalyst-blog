+++
date = "2016-08-21T11:19:56+08:00"
title = "外观模式"
categories = ["Scholar"]
tags = ["Pattern"]
description = "本文介绍外观模式"
slug = "design-pattern-facade"
+++

外观模式是一种使用频率非常高的结构型设计模式，它通过引入一个外观角色来简化客户端与子系统之间的交互，为复杂的子系统调用提供一个统一的入口，降低子系统与客户端的耦合度，且客户端调用非常方便。

比较一下自己泡茶和去茶馆喝茶的区别，如果是自己泡茶需要自行准备茶叶、茶具和开水，如图1(A)所示，而去茶馆喝茶，最简单的方式就是跟茶馆服务员说想要一杯什么样的茶，是铁观音、碧螺春还是西湖龙井？正因为茶馆有服务员，顾客无须直接和茶叶、茶具、开水等交互，整个泡茶过程由服务员来完成，顾客只需与服务员交互即可，整个过程非常简单省事，如图1(B)所示。

<img src="/images/design-pattern-facade-background.jpeg" alt="两种喝茶方式示意图" style="width: 500px;"/>

在软件开发中，有时候为了完成一项较为复杂的功能，一个客户类需要和多个业务类交互，而这些需要交互的业务类经常会作为一个整体出现，由于涉及到的类比较多，导致使用时代码较为复杂，此时，特别需要一个类似服务员一样的角色，由它来负责和多个业务类进行交互，而客户类只需与该类交互。外观模式通过引入一个新的外观类(Facade)来实现该功能，外观类充当了软件系统中的“服务员”，它为多个业务类的调用提供了一个统一的入口，简化了类与类之间的交互。在外观模式中，那些需要交互的业务类被称为子系统(Subsystem)。如果没有外观类，那么每个客户类需要和多个子系统之间进行复杂的交互，系统的耦合度将很大，如图2(A)所示；而引入外观类之后，客户类只需要直接与外观类交互，客户类与子系统之间原有的复杂引用关系由外观类来实现，从而降低了系统的耦合度，如图2(B)所示。

<img src="/images/design-pattern-facade-compare.jpeg" alt="外观模式示意图" style="width: 500px;"/>

### 基本定义

外观模式中，一个子系统的外部与其内部的通信通过一个统一的外观类进行，外观类将客户类与子系统的内部复杂性分隔开，使得客户类只需要与外观角色打交道，而不需要与子系统内部的很多对象打交道。

外观模式定义如下： 外观模式：为子系统中的一组接口提供一个统一的入口。外观模式定义了一个高层接口，这个接口使得这一子系统更加容易使用。

Facade Pattern: Provide a unified interface to a set of interfaces in a subsystem. Facade defines a higher-level interface that makes the subsystem easier to use.

外观模式又称为门面模式，它是一种对象结构型模式。外观模式是迪米特法则的一种具体实现，通过引入一个新的外观角色可以降低原有系统的复杂度，同时降低客户类与子系统的耦合度。

### 模式结构

外观模式没有一个一般化的类图描述，通常使用如图2(B)所示示意图来表示外观模式。图3所示的类图也可以作为描述外观模式的结构图：

![外观模式结构图](/images/design-pattern-facade.jpeg "Facade")

由图可知，外观模式包含如下两个角色：

1. Facade（外观角色）：在客户端可以调用它的方法，在外观角色中可以知道相关的（一个或者多个）子系统的功能和责任；在正常情况下，它将所有从客户端发来的请求委派到相应的子系统去，传递给相应的子系统对象处理。
2. SubSystem（子系统角色）：在软件系统中可以有一个或者多个子系统角色，每一个子系统可以不是一个单独的类，而是一个类的集合，它实现子系统的功能；每一个子系统都可以被客户端直接调用，或者被外观角色调用，它处理由外观类传过来的请求；子系统并不知道外观的存在，对于子系统而言，外观角色仅仅是另外一个客户端而已。

外观模式的主要目的在于降低系统的复杂程度，在面向对象软件系统中，类与类之间的关系越多，不能表示系统设计得越好，反而表示系统中类之间的耦合度太大，这样的系统在维护和修改时都缺乏灵活性，因为一个类的改动会导致多个类发生变化，而外观模式的引入在很大程度上降低了类与类之间的耦合关系。引入外观模式之后，增加新的子系统或者移除子系统都非常方便，客户类无须进行修改（或者极少的修改），只需要在外观类中增加或移除对子系统的引用即可。从这一点来说，外观模式在一定程度上并不符合开闭原则，增加新的子系统需要对原有系统进行一定的修改，虽然这个修改工作量不大。

外观模式中所指的子系统是一个广义的概念，它可以是一个类、一个功能模块、系统的一个组成部分或者一个完整的系统。子系统类通常是一些业务类，实现了一些具体的、独立的业务功能，其典型代码如下：

```java
class SubSystemA {
    public void MethodA() {
        //业务实现代码
    }
}

class SubSystemB {
    public void MethodB() {
        //业务实现代码
     }
}

class SubSystemC {
    public void MethodC() {
        //业务实现代码
    }
}
```

在引入外观类之后，与子系统业务类之间的交互统一由外观类来完成，在外观类中通常存在如下代码：

```java
class Facade {
    private SubSystemA obj1 = new SubSystemA();
    private SubSystemB obj2 = new SubSystemB();
    private SubSystemC obj3 = new SubSystemC();

    public void Method() {
        obj1.MethodA();
        obj2.MethodB();
        obj3.MethodC();
    }
}
```

由于在外观类中维持了对子系统对象的引用，客户端可以通过外观类来间接调用子系统对象的业务方法，而无须与子系统对象直接交互。引入外观类后，客户端代码变得非常简单，典型代码如下：

```java
public class Client {
    public static void main(String[] args) {
        EncryptFacade ef = new EncryptFacade();  
        ef.encrypt("src.txt", "des.txt");
    }
}
```

### 实现

下面通过一个应用实例来进一步学习和理解外观模式。

某软件公司欲开发一个可应用于多个软件的文件加密模块，该模块可以对文件中的数据进行加密并将加密之后的数据存储在一个新文件中，具体的流程包括三个部分，分别是读取源文件、加密、保存加密之后的文件，其中，读取文件和保存文件使用流来实现，加密操作通过求模运算实现。这三个操作相对独立，为了实现代码的独立重用，让设计更符合单一职责原则，这三个操作的业务代码封装在三个不同的类中。

#### 普通外观类

现使用外观模式设计该文件加密模块。

通过分析，本实例结构图如图所示。

<img src="/images/design-pattern-facade-example.jpeg" alt="文件加密模块结构图" style="width: 500px;"/>

在图中，EncryptFacade充当外观类，FileReader、CipherMachine和FileWriter充当子系统类。

EncryptFileReader：文件读取类，充当子系统类。

```java
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;

public class EncryptFileReader {
    public String read(String filename) {
        System.out.print("读取文件，获取明文：");

        StringBuilder buffer = new StringBuilder();
        File file = new File(filename);
        try (FileInputStream fis = new FileInputStream(file)) {

            int content;
            while ((content = fis.read()) != -1) {
                buffer.append((char) content);
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
        System.out.print(buffer.toString());

        return buffer.toString();
    }
}
```

CipherMachine：数据加密类，充当子系统类。

```java
public class CipherMachine {
    public String encrypt(String plainText) {
        System.out.print("数据加密，将明文转换为密文：");

        StringBuilder sb = new StringBuilder();
        char[] chars = plainText.toCharArray();
        for(char ch : chars) {
            sb.append(ch%7);
        }

        System.out.println(sb.toString());

        return sb.toString();
    }
}
```

EncryptFileWriter：文件保存类，充当子系统类。

```java
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;

public class EncryptFileWriter {

    public void write(String content, String filename) {
        System.out.println("保存密文，写入文件。");

        File file = new File(filename);
        try (FileOutputStream fop = new FileOutputStream(file)) {

            // if file doesn't exists, then create it
            // if (!file.exists()) {
            //     file.createNewFile();
            // }

            // get the content in bytes
            byte[] contentInBytes = content.getBytes();

            fop.write(contentInBytes);
            fop.flush();
            fop.close();

            System.out.println("Done");

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

EncryptFacade：加密外观类，充当外观类。

```java
public class EncryptFacade {
    private EncryptFileReader reader;
    private CipherMachine cipher;
    private EncryptFileWriter writer;

    public EncryptFacade() {
        reader = new EncryptFileReader();
        cipher = new CipherMachine();
        writer = new EncryptFileWriter();
    }

    //调用其他对象的业务方法
    public void encrypt(String from, String to) {
        String plainText = reader.read(from);
        String encryptText = cipher.encrypt(plainText);
        writer.write(encryptText, to);
    }
}
```

Client：客户端测试类

```java
public class Client {
    public static void main(String[] args) {
        EncryptFacade ef = new EncryptFacade();  
        ef.encrypt("src.txt", "des.txt");  
    }
}
```

编译并运行程序，输出结果如下：

```bash
读取文件，获取明文：Hello world!
数据加密，将明文转换为密文：2333640623253
保存密文，写入文件。
Done
```

在本实例中，对文件src.txt中的数据进行加密，该文件内容为“Hello world!”，加密之后将密文保存到另一个文件des.txt中，程序运行后保存在文件中的密文为“2333640623253”。在加密类CipherMachine中，采用求模运算对明文进行加密，将明文中的每一个字符除以一个整数（本例中为7，可以由用户来进行设置）后取余数作为密文。

#### 抽象外观类

在标准的外观模式结构图中，如果需要增加、删除或更换与外观类交互的子系统类，必须修改外观类或客户端的源代码，这将违背开闭原则，因此可以通过引入抽象外观类来对系统进行改进，在一定程度上可以解决该问题。在引入抽象外观类之后，客户端可以针对抽象外观类进行编程，对于新的业务需求，不需要修改原有外观类，而对应增加一个新的具体外观类，由新的具体外观类来关联新的子系统对象，同时通过修改配置文件来达到不修改任何源代码并更换外观类的目的。

下面通过一个具体实例来学习如何使用抽象外观类：

如果在应用实例“文件加密模块”中需要更换一个加密类，不再使用原有的基于求模运算的加密类CipherMachine，而改为基于移位运算的新加密类NewCipherMachine，其代码如下：

```java
public class NewCipherMachine {
    public String encrypt(String plainText) {
        System.out.print("数据加密，将明文转换为密文：");

        StringBuilder sb = new StringBuilder();
        int key = 10; // 设置密钥，移位数为10
        char[] chars = plainText.toCharArray();
        for (char ch : chars) {
            int temp = (int) ch;
            // 小写字母移位
            if(ch >= 'a' && ch <= 'z') {
                temp += key % 26;
                if(temp > 122) temp -= 26;
                if(temp < 97) temp += 26;
            }
            // 大写字母移位
            if(ch >= 'A' && ch <= 'Z') {
                temp += key % 26;
                if(temp > 90) temp -= 26;
                if(temp < 65) temp += 26;
            }

            sb.append((char)temp);
        }

        System.out.print(sb.toString());

        return sb.toString();
    }
}
```

如果不增加新的外观类，只能通过修改原有外观类EncryptFacade的源代码来实现加密类的更换，将原有的对CipherMachine类型对象的引用改为对NewCipherMachine类型对象的引用，这违背了开闭原则，因此需要通过增加新的外观类来实现对子系统对象引用的改变。

如果增加一个新的外观类NewEncryptFacade来与FileReader类、FileWriter类以及新增加的NewCipherMachine类进行交互，虽然原有系统类库无须做任何修改，但是因为客户端代码中原来针对EncryptFacade类进行编程，现在需要改为NewEncryptFacade类，因此需要修改客户端源代码。

如何在不修改客户端代码的前提下使用新的外观类呢？解决方法之一是：引入一个抽象外观类，客户端针对抽象外观类编程，而在运行时再确定具体外观类，引入抽象外观类之后的文件加密模块结构图如图所示：

<img src="/images/design-pattern-facade-example-abstract.jpeg" alt="引入抽象外观类之后的文件加密模块结构图" style="width: 500px;"/>

在图中，客户类Client针对抽象外观类AbstractEncryptFacade进行编程，AbstractEncryptFacade代码如下：

```java
public abstract class AbstractEncryptFacade {
    public abstract void encrypt(String from, String to);   
}
```

新增具体加密外观类NewEncryptFacade代码如下：

```java
public class NewEncryptFacade extends AbstractEncryptFacade {
    private EncryptFileReader reader;
    private NewCipherMachine cipher;
    private EncryptFileWriter writer;

    public NewEncryptFacade() {
        reader = new EncryptFileReader();
        cipher = new NewCipherMachine();
        writer = new EncryptFileWriter();
    }

    //调用其他对象的业务方法
    public void encrypt(String from, String to) {
        String plainText = reader.read(from);
        String encryptText = cipher.encrypt(plainText);
        writer.write(encryptText, to);
    }
}
```

配置文件config.xml中存储了具体外观类的类名，代码如下：

```xml
<?xml version="1.0" encoding="utf-8" ?>  
<config>  
    <className>NewEncryptFacade</className>  
</config>
```

读取XML的工具类：

```java
// 工具类XMLUtil.java
import javax.xml.parsers.*;
import org.w3c.dom.*;
import org.xml.sax.SAXException;
import java.io.*;

public class XMLUtil {
    // 该方法用于从XML配置文件中提取具体类类名，并返回一个实例对象
    public static Object getBean() {
        try {
            // 创建DOM文档对象
            DocumentBuilderFactory dFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = dFactory.newDocumentBuilder();
            Document doc;
            doc = builder.parse(new File("config.xml"));

            // 获取包含类名的文本节点
            NodeList nl = doc.getElementsByTagName("className");
            Node classNode = nl.item(0).getFirstChild();
            String cName = classNode.getNodeValue();

            // 通过类名生成实例对象并将其返回
            Class c = Class.forName(cName);
            Object obj = c.newInstance();
            return obj;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}
```

客户端测试代码修改如下：

```java
public class Client {
    public static void main(String[] args) {
        // EncryptFacade ef = new EncryptFacade();  
        // ef.encrypt("src.txt", "des.txt");
        AbstractEncryptFacade facade;
        // getBean()的返回类型为Object，需要进行强制类型转换
        facade = (AbstractEncryptFacade)XMLUtil.getBean();
        facade.encrypt("src.txt", "des.txt");
    }
}
```

编译并运行程序，输出结果如下：

```bash
读取文件，获取明文：Hello world!
数据加密，将明文转换为密文：Rovvy gybvn!
保存密文，写入文件。
```

原有外观类EncryptFacade也需作为抽象外观类AbstractEncryptFacade类的子类，更换具体外观类时只需修改配置文件，无须修改源代码，符合开闭原则。

### 总结

外观模式是一种使用频率非常高的设计模式，它通过引入一个外观角色来简化客户端与子系统之间的交互，为复杂的子系统调用提供一个统一的入口，使子系统与客户端的耦合度降低，且客户端调用非常方便。外观模式并不给系统增加任何新功能，它仅仅是简化调用接口。在几乎所有的软件中都能够找到外观模式的应用，如绝大多数B/S系统都有一个首页或者导航页面，大部分C/S系统都提供了菜单或者工具栏，在这里，首页和导航页面就是B/S系统的外观角色，而菜单和工具栏就是C/S系统的外观角色，通过它们用户可以快速访问子系统，降低了系统的复杂程度。所有涉及到与多个业务对象交互的场景都可以考虑使用外观模式进行重构。

#### 优点

外观模式的主要优点如下：

1. 它对客户端屏蔽了子系统组件，减少了客户端所需处理的对象数目，并使得子系统使用起来更加容易。通过引入外观模式，客户端代码将变得很简单，与之关联的对象也很少。
2. 它实现了子系统与客户端之间的松耦合关系，这使得子系统的变化不会影响到调用它的客户端，只需要调整外观类即可。
3. 一个子系统的修改对其他子系统没有任何影响，而且子系统内部变化也不会影响到外观对象。

#### 缺点

外观模式的主要缺点如下：

1. 不能很好地限制客户端直接使用子系统类，如果对客户端访问子系统类做太多的限制则减少了可变性和灵活性。
2. 如果设计不当，增加新的子系统可能需要修改外观类的源代码，违背了开闭原则。

#### 模式适用场景

在以下情况下可以考虑使用外观模式：

1. 当要为访问一系列复杂的子系统提供一个简单入口时可以使用外观模式。
2. 客户端程序与多个子系统之间存在很大的依赖性。引入外观类可以将子系统与客户端解耦，从而提高子系统的独立性和可移植性。
3. 在层次化结构中，可以使用外观模式定义系统中每一层的入口，层与层之间不直接产生联系，而通过外观类建立联系，降低层之间的耦合度。
