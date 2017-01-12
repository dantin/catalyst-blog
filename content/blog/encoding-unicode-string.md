+++
date = "2016-09-26T23:15:53+08:00"
title = "字符串，那些你不知道的事"
categories = ["Scholar"]
tags = ["OS", "JVM"]
description = "本文描述字符串编码的相关概念"
slug = "encoding-unicode-string"
+++

也许你会诧异，字符串有什么难的，即便遇到乱码的情况随便Google下就能找到解决方法，但是这样你不觉得有种被动的感觉嘛，我觉得和学习任何东西一样，学习编程首要是学习其思想，知道某事物为什么（why）要这么做，至于如何做（how）那只是前人提出的解决方案，我们可以参考，顺便掌握下来。

本文下面首先讲解字符、字符串、编码、ASCII、Unicode、UTF-8 等一些基本概念，然后会简单介绍在使用计算机时是如何与编码打交道的。 希望在阅读完本文后，能对string有一全新的认识。

### 为什么需要字符编码

当我们谈到字符串（string或text）时，你可能会想到“计算机屏幕上的那些字符（characters）与符号（symbols）”，你正在阅读的文章，无非也是由一串字符组成的。但是你也许会发现，你无法给“字符串”一明确定义，但是我们就是知道，就像给你一个苹果，你能说出其名字，但是不能给出准确定义一样。这个问题先放一放，后面我再解释。

我们知道，计算机并不能直接处理操作字符与符号，它只认识 0、1 这两个数字，所以如果想让计算机显示各种各样的字符与符号，就必须定义它们与数字的一一映射关系，也就是我们所熟知的字符编码（character encoding）。你可简单的认为，字符编码为计算机屏幕上显示的字符与这些字符保存在内存或磁盘中的形式提供了一种映射关系。字符编码纷繁复杂，有些专门为特定语言优化，像针对简体中文的编码就有[EUC-CN](https://en.wikipedia.org/wiki/Extended_Unix_Code#EUC-CN)，[HZ](https://en.wikipedia.org/wiki/HZ_%28character_encoding%29)；针对日文的[EUC-JP](https://en.wikipedia.org/wiki/Extended_Unix_Code#EUC-JP)，针对英文的[ASCII](https://en.wikipedia.org/wiki/ASCII)；另一些专门用于多语言环境，像后面要讲到的[UTF-8](https://en.wikipedia.org/wiki/UTF-8)。

我们可以把字符编码看作一种解密密钥（decryption key），当我们收到一段字节流时，无论来自文件还是网络，如果我们知道它是“文本（text）”，那么我们就需要知道采用何种字符编码来解码这些字节流，否则，我们得到的只是一堆无意义的符号，像 ������。

### 单字节编码

计算机最早起源于以英文为母语的美国，英文中的符号比较少，用七个二进制位就足以表示，现在最常见也是最流行的莫过于ASCII编码，该编码使用0到127之间的数字来存储字符（65表示“A”，97表示“a”）。

<img src="/images/unicode-string-01.jpeg" alt="USASCII code chart" style="width: 455px;"/>

我们知道一个字节是8位，ASCII编码其实只使用了其中的低7位，还剩下1位。很多人就想着可以利用这最高的一位来表示更多的可见字符，由于 IBM是那时最有名的OEM，其制定的编码规则影响范围也最广。

![IBM OEM ASCII](/images/unicode-string-02.gif "IBM OEM ASCII")

随着时间的推进，计算机的使用范围扩展到西方欧洲国家，像法国、西班牙，德国等，它们这些国家的字母比英文要多。所以为了表示这些国家的语言，也需要借助最高位扩展ASCII编码。但由于没有统一的标准，有些地方用130表示é，有些地方表示为Hebrew letter Gimel ג。在这些语言中，使用最广的是CP-1252编码，也称为[Windows-1252编码](https://en.wikipedia.org/wiki/Windows-1252)，因为在[Windows在1.0时就使用了该编码](https://en.wikipedia.org/wiki/Windows-1252#History)，随着Windows的普及，大家就沿用了Windows-1252的说法。

![Windows-1252](/images/unicode-string-03.jpg "Windows-1252")

### ISO-8859-1

既然说到了Windows-1252，那么就不能不提它与ISO-8859-1的关系，我相信大家对ISO-8859-1这个编码肯定很熟悉，我还记得第一次用Dreamweaver写HTML时，其HTML模板中默认编码就是ISO-8859-1，还有一个比较常见的场景是在MySQL中，MySQL的默认编码为latin-1，这其实是ISO-8859-1的一个别名而已。

[ISO-8859-1](https://en.wikipedia.org/wiki/ISO/IEC_8859-1)是早期 8 位编码方案的一种，是[ISO/IEC 8859](https://en.wikipedia.org/wiki/ISO/IEC_8859)编码系列的一种，第一版发布于1987年。它主要是针对西欧国家设计，现在大多数流行的8位编码方案都以它为基础，这其中就包括Windows-1252。

Windows-1252与ISO-8859-1的主要不同在于0x80到0x9F之间的字符，在ISO-8859-1中为控制字符（control characters），在Windows-1252中为可打印字符（printable characters）。

在HTTP协议中，以`text/`开头的MIME类型的文件默认编码为ISO-8859-1，但是由于控制字符在文件中用处不大，所以大多数客户端程序用Windows-1252来解码，这也就是它们之间经常混淆的主要原因。

### 字符集 vs 字符编码

在介绍完ASCII之后，需要强调一个很重要但被大多数人都忽略的一个概念问题。

我们平时说的ASCII其实有两个含义，一个是ASCII字符集，另一个是ASCII编码。

> ASCII字符集只是定义了字符与字符码（character code，也称code point代码点）的对应关系。也就是说这一层面只是规定了字符A用65表示，至于这个65在内存或硬盘中怎么表示，它不管，那是ASCII编码做的事。
> 
> ASCII编码规定了用7个二进制位来保存ASCII字符码，即定义了字符集的存储形式。

说到这里你也许会问，那既然用7个二进制位就能够表示所有ASCII字符码了，为什么现在一个字节是8位，而不是7位呢，这不是浪费吗？

其实这是早期设计者有意而为之：

> 7位表示ASCII字符码，剩下1位为[Parity bit](https://en.wikipedia.org/wiki/Parity_bit)，也称为校验位，用以检查数据的正确性。

关于数据校验，我这里不打算展开讲，感兴趣的可以参考[Error detection and correction](https://en.wikipedia.org/wiki/Error_detection_and_correction)。

为了让大家更清楚的明白这两者以及相关概念的关系，我画了图，便于大家理解。

![Charset & Encoding](/images/unicode-string-04.png "Charset And Encoding")

* Character字符。即我们看到的单个符号，像“A”、“啊”等
* Code point代码点。一个无符号数字，通常用16进制表示。代码点与字符的一一对应关系称为字符集（Character Set），这种对应关系肯定不止一种，也就导致了不同字符集的出现，像ASCII、ISO-8859-1、GB2312、GBK、Unicode 等。
* Bytes二进制字节。其含义为代码点在内存或磁盘中的表示形式。代码点与二进制字节的一一对应关系称为编码（Encoding），当然这种对应关系也不是唯一的，所以编码也有很多种，像ASCII、ISO-8859-1、ENC-CN、GBK、UTF-8等。

> 上面这个图基本把我们平时经常混淆的概念清晰地区分开了，大家一定要充分理解并牢记于心。

### 多字节编码

多字节编码主要用于我们亚洲国家，像中文（Chinese），日文（Japanese），韩文（Korean）（业界一般称为 CJK）等象形（表意）文字（ideograph-based language），字符数量比较多，1个字节是放不下的，所以需要更多的字节来进行字符的编码。

[ISO/IEC 2022](https://en.wikipedia.org/wiki/ISO/IEC_2022)标准为多字节编码制定了一套标准，主要有下面两个方面：

1. 一个编码系统里面可以表示多种字符集
2. 一个编码系统既可以在7位编码系统中表示所有字符集，也可以在8位编码系统表示所有字符集

为了能够表示多种字符集ISO/IEC 2022引入了[escape sequences](https://en.wikipedia.org/wiki/Escape_sequence)，也就是我们中文里面说的“转义字符”的意思；为了能够兼容之前的7位编码系统，像ASCII，实现ISO/IEC 2022标准的编码系统一般都是__变长编码__。

#### GB2312

GB2312是我国国家标准总局在1980年发布一套遵循ISO/IEC 2022标准的字符集，在GB2312中，字符码一般称为区位码，由于该字符集需要兼容ASCII字符集，所以它只能一个字节中的7位，剩下1位用于区分，比如可以通过最高位为1表示GB2312字符集，为0表示ASCII字符集。

GB2312使用两个字节来表示字符码，最多可以表示94 * 94个字符，但是GB2312并没有全部使用，留了一部分方便后面扩展用。

实现GB2312字符集的编码主要是EUC-CN，该编码与ASCII编码兼容。

我们平时说的GB2312编码其实就是指的EUC-CN编码，这一点需要明白。

#### GBK

GBK字符集是对GB2312字符集的扩展，GBK并没有一个官方标准，现在使用最广的标准是微软在Windows 95中实现的版本——[CP936](https://en.wikipedia.org/wiki/Code_page_936)编码。

GBK也使用两个字节来表示字符码，94 * 94 的区位码分布可以参考下面这个图，截自[Wikipedia](https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/GBK_encoding.svg/1290px-GBK_encoding.svg.png)

![GBK](/images/unicode-string-05.jpg "GBK")

同GB2312一样，我们平时说的GBK编码其实就是指的CP936编码。

除了我们中国的GB*系统字符集以外，日本、韩国各有各的字符集标准，虽然都是基于ISO/IEC 2022，但是具体的表示方式千差万别，比如1601在GB2312中表示“啊”，但在日韩就不知道表示什么含义了。

所以，我们需要一种囊括世界上所有字符的一套字符集，在该字符集中，字符码与字符一一对应，比如字符码0x41表示英文字母A，在任何国家都表示A，即使该国家没有这个字符。解决这个问题的是现在最流行的一套字符集——Unicode。

### Unicode

Unicode的全称是universal character encoding，中文一般翻译为“统一码、万国码、单一码”。

![Unicode](/images/unicode-string-06.jpg "Unicode")

在Unicode中字符码称为code point，用4个字节来表示，这么做主要是为了涵盖世界上所有的字符。写法一般为U+XXXX，XXXX 为用 16 进制表示的数字。比如，U+0041表示A。

#### Unicode的存储形式

Unicode的存储形式一般称为UTF-*编码，其中UTF全称为Unicode Transformation Format，常见的有：

#### UTF-32

UTF-32编码是Unicode最直接的存储方式，用4个字节来分别表示code point中的4个字节，也是UTF-*编码家族中唯一的一种__定长编码（fixed-length encoding）__。UTF-32的好处是能够在O(1)时间内找到第N个字符，因为第N个字符的编码的起点是N*4个字节，当然，劣势更明显，四个字节表示一个字符，别说以英文为母语的人不干，我们中国人也不干了。

#### UTF-16

UTF-16最少可以采用2个字节表示code point，需要注意的是，UTF-16是一种__变长编码（variable-length encoding）__，只不过对于65535之内的code point，采用2个字节表示而已。如果想要表示65535之上的字符，需要一些hack的手段，具体可以参考[wiki UTF-16#U.2B10000toU.2B10FFFF](https://en.wikipedia.org/wiki/UTF-16#U.2B10000_to_U.2B10FFFF)。很明显，UTF-16比UTF-32节约一半的存储空间，如果用不到65535之上的字符的话，也能够在O(1)时间内找到第 N 个字符。

> UTF-16与UTF-32还有一个不明显的缺点。我们知道不同的计算机存储字节的顺序是不一样的，这也就意味着U+4E2D 在UTF-16可以保存为`4E 2D`，也可以保存成`2D 4E`，这取决于计算机是采用大端模式还是小端模式，UTF-32的情况也类似。为了解决这个问题，引入了__BOM (Byte Order Mark)__，它是一特殊的不可见字符，位于文件的起始位置，标示该文件的字节序。对于UTF-16来说，BOM为`U+FEFF`（FF 比 FE 大 1），如果UTF-16编码的文件以`FF FE`开始，那么就意味着其字节序为小端模式，如果以`FE FF`开始，那么就是大端模式。其他UTF-*编码的BOM可以参考[Representations of byte order marks by encoding](https://en.wikipedia.org/wiki/Byte_order_mark#Representations_of_byte_order_marks_by_encoding)。

#### UTF-8

UTF-16对于以英文为母语的人来说，还是有些浪费了，这时聪明的人们（准确说是[Ken Thompson](https://en.wikipedia.org/wiki/Ken_Thompson_%28computer_programmer%29)与[Rob Pike](https://en.wikipedia.org/wiki/Rob_Pike)）又发明了另一个编码——[UTF-8](https://en.wikipedia.org/wiki/UTF-8)。在UTF-8中，ASCII字符采用单字节。其实，UTF-8前128个字符与ASCII字符编码方式一致；扩展的拉丁字符像ñ、ö等采用2个字节存储；中文字符采用3个字符存储，使用频率极少字符采用4个字节存储。由此可见，UTF-8也是一种__变长编码（variable-length encoding）__。

UTF-8的编码规则很简单，只有二条： 
1. 对于单字节的符号，字节的第一位设为0，后面7位为这个符号的code point。因此对于英语字母，UTF-8编码和ASCII码是相同的。 
2. 对于n字节的符号，第一个字节的前n位都设为1，第n+1位设为0，后面字节的前两位一律设为10。剩下的没有提及的二进制位，全部为这个符号的code point。

<img src="/images/unicode-string-07.png" alt="UTF-8编码规则" style="width: 455px;"/>

通过上面这两个规则，UTF-8就不存在字节顺序在大小端不同的情况，所以用UTF-8编码的文件在任何计算机中保存的字节流都是一致的，这是其很重要一优势；UTF-8的另一大优势在于对ASCII字符超节省空间，存储扩展拉丁字符与UTF-16的情况一样，存储汉字字符比UTF-32更优。

UTF-8的一劣势是查找第N个字符时需要O(N)的时间，也就是说，字符串越长，就需要更长的时间来查找其中的每个字符。其次是在对字节流解码、字符编码时，需要遵循上面两条规则，比UTF-16、UTF-32略麻烦。

随着互联网的兴起，UTF-8是逐渐成为使用范围最广的编码方案。下图为Google在2010年初做的[统计](http://googleblog.blogspot.com/2010/01/unicode-nearing-50-of-web.html)（链接需翻墙）

<img src="/images/unicode-string-08.jpg" alt="Growth of Unicode on the Web" style="width: 455px;"/>

由于 Google 的爬虫遍布全世界，这个数据可信度比较高。

#### UCS

我们在互联网上查找编码相关资料时，经常会看到UCS-2、UCS-4编码，它们和UTF-*编码家族是什么关系呢？要想理清它们之间的关系，需要先弄清楚，什么是__UCS__。

[UCS](https://en.wikipedia.org/wiki/Universal_Coded_Character_Set)全称是__Universal Coded Character Set__，是由ISO/IEC 10646定义的一套标准字符集，是很多字符编码的基础，UCS中大概包含100,000个抽象字符，每一个字符都有一唯一的数字编码，称为code point。

在19世纪八十年代晚期，有两个组织同时在UCS的基础上开发一种与具体语言无关的统一的编码方案，这两个组织分别是[IEEE](https://en.wikipedia.org/wiki/IEEE)与[Unicode Consortium](https://en.wikipedia.org/wiki/Unicode_Consortium)，为了保持这两个组织间编码方案的兼容性，两个组织尝试着合作。早期的两字节编码方案叫做“Unicode”，后来改名为“UCS-2”，在研发过程发，发现16位根本不能够囊括所有字符，于是IEEE引入了新的编码方案——UCS-4 编码，这种编码每个字符需要4个字节，这一行为立刻被Unicode Consortium制止了，因为这种编码太浪费空间了，又因为一些设备厂商已经对2字节编码技术投入大量成本，所以在1996年7月发布的Unicode 2.0 中提出了UTF-16来打破UCS-2与UCS-4之间的僵局，UTF-16在2000年被[IEFE](https://en.wikipedia.org/wiki/IETF)组织制定为[RFC 2781](https://tools.ietf.org/html/rfc2781)标准。

由此可见，UCS-*编码是一历史产物，目前来说，统一编码方案最终的赢家是UTF-*编码。

### 实战

#### 操作系统

根据[UTF-16 FOR PROCESSING](http://unicode.org/notes/tn12/#Software_16)，现在流行的三大操作系统Windows、Mac、Linux均采用UTF-16编码方案，上面链接也指出，现代编程语言像Java、ECMAScript、.Net平台上所有语言等在内部也都使用UTF-16来表示字符。

<img src="/images/unicode-string-09.png" alt="Mac UTF-16" style="width: 455px;"/>

上图为Mac系统中文件浏览器Finder的界面，其中所有的字符，在内存中都是以UTF-16的编码方式存储的。

你也许会问，为什么操作系统都这么偏爱UTF-16，Stack Exchange上面有一个精彩的回答，感兴趣的可以去了解

[Should UTF-16 be considered harmful?](http://programmers.stackexchange.com/questions/102205/should-utf-16-be-considered-harmful)
[UTF-8 Everywhere](http://utf8everywhere.org/)

#### Locale

为了适应多语言环境，Linux/Mac系统通过locale来设置系统的语言环境，下面是在Mac终端输入locale得到的输出

```bash
LANG="en_US.UTF-8"         <==主语言的环境
LC_COLLATE="en_US.UTF-8"   <==字串的比较排序等
LC_CTYPE="en_US.UTF-8"     <==语言符号及其分类
LC_MESSAGES="en_US.UTF-8"  <==信息显示的内容，如功能表、错误信息等
LC_MONETARY="en_US.UTF-8"  <==币值格式的显示等
LC_NUMERIC="en_US.UTF-8"   <==数字系统的显示信息
LC_TIME="en_US.UTF-8"      <==时间系统的显示资料
LC_ALL="en_US.UTF-8"       <==语言环境的整体设定
```

locale按照所涉及到的文化传统的各个方面分成12个大类，上面的输出只显示了其中的6类。为了设置方便，我们可以通过设置LC_ALL、LANG来改变这12个分类熟悉。其优先级关系为

> LC_ALL > LC_* > LANG

设置好locale，操作系统在进行文本字节流解析时，如果没有明确制定其编码，就用locale设定的编码方案，当然现在的操作系统都比较聪明，在用默认编码方案解码不成功时，会尝试其他编码，现在比较成熟的编码测探技术有[Mozila的UniversalCharsetDetection](http://www-archive.mozilla.org/projects/intl/UniversalCharsetDetection.html)与[ICU的Character Set Detection](http://userguide.icu-project.org/conversion/detection)。

#### Java

一般来说，高级编程语言都提供都对字符的支持，像Java中的[Character](http://docs.oracle.com/javase/7/docs/api/java/lang/Character.html)类就采用UTF-16编码方案。

这里有个文字游戏，一般我们说“某某字符串是XX编码”，其实这是不合理的，因为字符串压根就没有编码这一说法，只有字符才有，字符串只是字符的一串序列而已。 不过我们平时并没有这么严谨，不过你要明白，当我们说“某某字符串是XX编码”时，知道这其实指的是该字符串中字符的编码就可以了。 这也就回答了本文一开始提到问题，什么是字符串：

> Bytes are not character, bytes are bytes. Characters are an abstraction. A string is a sequence of those abstraction.

我们可以做个简单的实验来验证Java中确实使用UTF-16编码来存储字符：

```java
public class EncodingTest {  
    public static void main(String[] args) {
        String s  = "中国人a";
        try {
            //线程睡眠，阻止线程退出
            Thread.sleep(10000000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```

在使用javac编译这个类时，javac会按照操作系统默认的编码去解析字节流，如果你保存的源文件编码与操作系统默认不一致，是可能出错的，可以在启动javac命令时，附加`-encoding <encoding>`选项来指明源代码文件所使用的编码。

```bash
# 编译生成.class文件
javac -encoding utf-8 EncodingTest.java  
# 执行该类
java EncodingTest  
# 使用jps查看其pid，然后用jmap把程序运行时内存的内容dump下来
jmap -dump:live,format=b,file=encoding_test.bin <pid>  
# 在Linux/Mac 系统上，使用xxd命令以十六进制查看该文件，这里用管道传给了vim
xxd encoding_test.bin | vim -  
```

<img src="/images/unicode-string-10.png" alt="Java UTF-16" style="width: 455px;"/>

其中用红框标注部分就是上面EncodingTest类中字符串s的内容，4e2d是“中”的code point，56fd是“国”的code point，4eba是“人”的code point，0061是“a”的code point。而在UTF-16编码中，0-66535之间的字符直接用两个字节存储，这也就证明了Java中的Character是使用UTF-16编码的。

#### Python

首先说下Python解释器如何解析Python源程序。

在Python 2中，Python解析器默认用ASCII编码来读取源程序，当程序中包含非ASCII字符时，解释器会报错，下面实验在Mac上用python 2.7.6进行：

```bash
$ cat str.py
#!/usr/bin/env python
a = "中国人"

$ python str.py
  File "str.py", line 2
SyntaxError: Non-ASCII character '\xe4' in file str.py on line 2, but no encoding declared; see http://www.python.org/peps/pep-0263.html for details  
```

可以通过在源程序起始处用`coding: name`或`coding=name`来声明源程序所用的编码。

Python 3中改变了这一行为，解析器默认采用UTF-8解析源程序。

按理接下来应该介绍Python中对字符的处理了，但介于本文篇幅，这里不再介绍，后面会单独写篇文章进行介绍。感兴趣的可以先参考下面的文章： - [More About Unicode in Python 2 and 3](http://lucumr.pocoo.org/2014/1/5/unicode-in-2-and-3/)

#### JavaScript

[JavaScript’s internal character encoding: UCS-2 or UTF-16?](https://mathiasbynens.be/notes/javascript-encoding)

#### HTML/XML

在Web浏览器接收到来自世界各地的HTML/XML时，也需要正确的编码方案才能够正常显示网页，在现代的HTML5页面，一般通过下面的代码指定

```html
<meta charset="UTF-8">  
```

4.0.1之前的HTML页面使用下面的代码

```html
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">  
```

XML使用属性标注其编码

```xml
<?xml version="1.0" encoding="UTF-8" ?>  
```

仔细想想，这里有个矛盾的地方，因为我们需要事先知道某字节流的编码才能正确解析该字节流，而这个字节流的编码是保存在这段字节流中的，和“鸡生蛋，蛋生鸡”的问题有点像，其实这并不是一个问题，因为大部分的编码都是兼容ASCII编码的，而这些HTML/XML开始处基本都是ASCII字符，所以采用浏览器默认的编码方案即可解析出该字节流所声明的编码，在解析出该字节流所用编码后，使用该编码重新解析该字节流即可。

### 总结

通过上面的分析讲解，我相信大部分人都会string产生了一新的认识。计算机中有很多我们认为理所当然的事，但事实一般并非如此，希望本文能对大家理解计算机有抛砖引玉的作用。

参考

* [The Absolute Minimum Every Software Developer Absolutely, Positively Must Know About Unicode and Character Sets (No Excuses!)](http://www.joelonsoftware.com/articles/Unicode.html)
* [《Dive Into Python 3》 Chapter 4. Strings](http://www.diveintopython3.net/strings.html)
* [字符编码笔记：ASCII，Unicode和UTF-8](http://www.ruanyifeng.com/blog/2007/10/ascii_unicode_and_utf-8.html)
* [Java: a rough guide to character encoding](http://illegalargumentexception.blogspot.hk/2009/05/java-rough-guide-to-character-encoding.html)
* [有赞技术博客](http://tech.youzan.com/strings/)
