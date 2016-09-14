---
title: 从JAR包中读取资源文件
date: 2016-09-12 10:15:05
categories: 工程
tags: Java
toc: true
---

通常在代码中读取一些资源文件(比如图片，音乐，文本等等)。在单独运行的时候这些简单的处理当然不会有问题。

但是，如果把代码打成一个jar包以后，即使将资源文件一并打包，这些东西也找不出来了。

```java
//源代码1：  
package edu.hxraid;
import java.io.*;
public class Resource {
    public  void getResource() throws IOException{
        File file=new File("bin/resource/res.txt");
        BufferedReader br=new BufferedReader(new FileReader(file));
        String s="";
        while((s=br.readLine())!=null)
            System.out.println(s);
    }
}
```

### 问题代码

这段代码写在Eclipse建立的java Project中，其目录为：(其中将资源文件res.txt放在了bin目录下，以便打成jar包)

```bash
src/
src/edu/hxraid/Resource.java
bin/
bin/resource/res.txt
bin/edu/hxraid/Resource.class
```

很显然运行源代码1是能够找到资源文件res.txt。但当我们把整个工程打成jar包以后(ResourceJar.jar)，这个jar包内的目录为：

```bash
edu/hxraid/Resource.class
resource/res.txt
```

而这时jar包中Resource.class字节码：ldc <String "bin/resource/res.txt"> [20] 将无法定位到jar包中的res.txt位置上。就算把bin/目录去掉：ldc <String "resource/res.txt"> [20] 仍然无法定位到jar包中res.txt上。

这主要是因为jar包是一个单独的文件而非文件夹，绝对不可能通过"file:/e:/.../ResourceJar.jar/resource /res.txt"这种形式的文件URL来定位res.txt。所以即使是相对路径，也无法定位到jar文件内的txt文件(读者也许对这段原因解释有些费解，在下面我们会用一段代码运行的结果来进一步阐述)。

### ClassLoader

那么把资源打入jar包，无论ResourceJar.jar在系统的什么路径下，jar包中的字节码程序都可以找到该包中的资源。这会是幻想吗？

当然不是，我们可以用类装载器(ClassLoader)来做到这一点：

ClassLoader 是类加载器的抽象类。它可以在运行时动态的获取加载类的运行信息。 可以这样说，当我们调用ResourceJar.jar中的Resource类时，JVM加载进Resource类，并记录下Resource运行时信息(包括Resource所在jar包的路径信息)。

而ClassLoader类中的方法可以帮助我们动态的获取这些信息:

* public URL getResource(String name) 
    查找具有给定名称的资源。资源是可以通过类代码以与代码基无关的方式访问的一些数据(图像、声音、文本等)。并返回资源的URL对象。
* public InputStream getResourceAsStream(String name); 
    返回读取指定资源的输入流。这个方法很重要，可以直接获得jar包中文件的内容。

ClassLoader是abstract的，不可能实例化对象，更加不可能通过ClassLoader调用上面两个方法。所以我们真正写代码的时候，是通过Class类中的getResource()和getResourceAsStream()方法，这两个方法会委托ClassLoader中的getResource()和getResourceAsStream()方法 。

好了，现在我们重新写一段Resource代码,来看看上面那段费解的话是什么意思了：

```java
//源代码2：  
package edu.hxraid;
import java.io.*;
import java.net.URL;
public class Resource {
    public  void getResource() throws IOException{
              //查找指定资源的URL，其中res.txt仍然开始的bin目录下
        URL fileURL=this.getClass().getResource("/resource/res.txt");
        System.out.println(fileURL.getFile());
    }
    public static void main(String[] args) throws IOException {
        Resource res=new Resource();
        res.getResource();
    }
}
```

运行这段源代码结果：/E:/Code_Factory/WANWAN/bin/resource/res.txt  (../ Code_Factory/WANWAN/.. 是java project所在的路径)

我们将这段代码打包成ResourceJar.jar ,并将ResourceJar.jar放在其他路径下(比如 c:\ResourceJar.jar)。然后另外创建一个java project并导入ResourceJar.jar，写一段调用jar包中Resource类的测试代码：

```java
import java.io.IOException;
import edu.hxraid.Resource;
public class TEST {
    public static void main(String[] args) throws IOException {
        Resource res=new Resource();
        res.getResource();
    }
}
```

这时的运行结果是：file:/C:/ResourceJar.jar!/resource/res.txt
 
我们成功的在运行时动态获得了res.txt的位置。然而，问题来了，你是否可以通过下面这样的代码来得到res.txt文件？

```java
File f=new File("C:/ResourceJar.jar!/resource/res.txt");
```

当然不可能，因为".../ResourceJar.jar!/resource/...."并不是文件资源定位符的格式 (jar中资源有其专门的URL形式： jar:<url>!/{entry} )。所以，如果jar包中的类源代码用File f=new File(相对路径);的形式，是不可能定位到文件资源的。这也是为什么源代码1打包成jar文件后，调用jar包时会报出FileNotFoundException的症结所在了。

### Resource Stream

我们不能用常规操作文件的方法来读取ResourceJar.jar中的资源文件res.txt，但可以通过Class类的getResourceAsStream()方法来获取 ，这种方法是如何读取jar中的资源文件的，这一点对于我们来说是透明的。我们将Resource.java改写成：

```java
//源代码3：  
package edu.hxraid;  
import java.io.*;  
public class Resource {  
    public void getResource() throws IOException{  
        //返回读取指定资源的输入流  
        InputStream is=this.getClass().getResourceAsStream("/resource/res.txt");   
        BufferedReader br=new BufferedReader(new InputStreamReader(is));  
        String s="";  
        while((s=br.readLine())!=null)  
            System.out.println(s);  
    }  
}
```

我们将java工程下/bin目录中的edu/hxraid/Resource.class和资源文件resource/res.txt一并打包进ResourceJar.jar中，不管jar包在系统的任何目录下，调用jar包中的Resource类都可以获得jar包中的res.txt资源，再也不会找不到res.txt文件了。

参考
[ITEYE](http://hxraid.iteye.com/blog/483115)