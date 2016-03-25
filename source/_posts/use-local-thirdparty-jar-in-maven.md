title: 在Maven中使用本地第三方Jar包
date: 2016-03-24 17:11:17
categories: 学习
tags: [Maven]
toc: true
---

对于一些特殊的依赖包，可能不同的开发者有着特殊的jar文件，针对于这种情况按以下方式解决：

### POM配置

在应用的根pom.xml文件中加入下面的配置：

```xml
<repositories>
        <repository>
            <id>local-project-third-party</id>
            <name> Third Party Repository</name>
            <url>
                file://${project.basedir}/third-party
            </url>
        </repository>
</repositories>
```

其中`${project.basedir}`表示应用的根路径，是maven的内置参数，无需修改。在项目使用jar文件的模块的根目录下创建一个third-party文件夹，之后按照jar包所在的文件夹创建jar文件路径。例如有依赖描述如下：

```xml
<dependency>
    <groupId>com.taobao.sdk</groupId>
    <artifactId>taobao-sdk-java-auto_1458614641006</artifactId>
    <version>20160324</version>
</dependency>
```
那么就需要在third-party目录下依次创建com、taobao、sdk、taobao-sdk-java-auto_1458614641006、20160324文件夹，jar文件放入20160324文件夹中，目录结构如下：

```bash
com/taobao/sdk/taobao-sdk-java-auto_1458614641006
```

__注意：当项目有多个模块构成，third-party文件夹不是放在整个项目的父模块的根目录中，而是放在需要使用定制jar包的模块的根目录下。__
