+++
date = "2016-01-15T11:09:40+08:00"
title = "Python包管理工具setuptools"
categories = ["Engineering"]
tags = ["Python", "Setuptools"]
description = "本文介绍Python的包管理工具setuptools"
slug = "python-setuptools"
+++

Setuptools是Python distutils增强版的集合，它可以帮助我们更简单的创建和分发Python包，尤其是拥有依赖关系的。用户在使用setuptools创建的包时，并不需要已安装setuptools，只要一个启动模块即可。

功能亮点：

* 利用EasyInstall自动查找、下载、安装、升级依赖包
* 创建Python Eggs
* 包含包目录内的数据文件
* 自动包含包目录内的所有的包，而不用在setup.py中列举
* 自动包含包内和发布有关的所有相关文件，而不用创建一个MANIFEST.in文件
* 自动生成经过包装的脚本或Windows执行文件
* 支持Pyrex，即在可以setup.py中列出.pyx文件，而最终用户无须安装Pyrex
* 支持上传到PyPI
* 可以部署开发模式，使项目在sys.path中
* 用新命令或setup()参数扩展distutils，为多个项目发布/重用扩展
* 在项目setup()中简单声明entry points，创建可以自动发现扩展的应用和框架

### 安装

通常setuptools都是自带的，若需要安装，可以使用如下命令

``` Bash
pip install setuptools
```

### 创建包

有了setuptools后，创建一个包通常是先建一个目录

``` Bash
cd /tmp 
mkdir demo
cd demo
```

在demo中创建一个setup.py文件

``` Python
from setuptools import setup, find_packages

setup(
        name='demo',
        version="0.1",
        packages=find_packages(),
)
```

执行python setup.py bdist_egg即可打包一个test的包了。

``` Bash
demo
├── build
│   └── bdist.macosx-10.10-intel
├── demo.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   └── top_level.txt
├── dist
│   └── demo-0.1-py2.7.egg
└── setu
```

在dist中生成的是egg包

``` Bash
file dist/demo-0.1-py2.7.egg
dist/demo-0.1-py2.7.egg: Zip archive data, at least v2.0 to extract
```

看一下生成的.egg文件，是个zip包。

``` Bash
upzip -l dist/demo-0.1-py2.7.egg

Archive:  dist/demo-0.1-py2.7.egg
  Length     Date   Time    Name
 --------    ----   ----    ----
        1  01-15-16 11:23   EGG-INFO/dependency_links.txt
      176  01-15-16 11:23   EGG-INFO/PKG-INFO
      120  01-15-16 11:23   EGG-INFO/SOURCES.txt
        1  01-15-16 11:23   EGG-INFO/top_level.txt
        1  01-15-16 11:23   EGG-INFO/zip-safe
 --------                   -------
      299                   5 files
```

包里面是一系列自动生成的文件。

setup()中的参数：

* name 包名
* version 版本号
* packages 所包含的其他包

要想发布到PyPI中，需要增加别的参数，这个可以参考[官方文档](http://pythonhosted.org/setuptools/setuptools.html#basic-use)中的例子了。

### 增加内容

上面生成的egg中没有实质的内容，显然谁也用不了，现在稍微调色一下，增加一点内容。

在demo中执行mkdir demo，再创建一个目录，在这个demo目录中创建一个__init__.py的文件，表示这个目录是一个包，然后写入：

``` Python
#!/usr/bin/env python
#-*- coding:utf-8 -*-

def test():
    print "hello world!"  

if __name__ == '__main__':
    test()
```

现在的主目录结构为下：

``` Bash
demo
├── demo
│   └── __init__.py
└── setup.py
```

再次执行python setup.py bdist_egg后，再看egg包


``` Bash
unzip -l dist/demo-0.1-py2.7.egg

Archive:  dist/demo-0.1-py2.7.egg
  Length     Date   Time    Name
 --------    ----   ----    ----
      122  01-15-16 11:32   demo/__init__.py
      354  01-15-16 11:34   demo/__init__.pyc
        1  01-15-16 11:34   EGG-INFO/dependency_links.txt
      176  01-15-16 11:34   EGG-INFO/PKG-INFO
      137  01-15-16 11:34   EGG-INFO/SOURCES.txt
        5  01-15-16 11:34   EGG-INFO/top_level.txt
        1  01-15-16 11:34   EGG-INFO/zip-safe
 --------                   -------
      796                   7 files
```

这回包内多了demo目录，显然已经有了我们自己的东西了，安装体验一下。

``` Bash
python setup.py install
```

这个命令会讲我们创建的egg安装到python的dist-packages目录下，位置在

```console
/Users/david/Documents/venv/test/lib/python2.7/site-packages/demo-0.1-py2.7.egg
```

查看一下它的结构：

``` Bash
/Users/david/Documents/venv/test/lib/python2.7/site-packages/demo-0.1-py2.7.egg
|-- demo
|   |-- __init__.py
|   `-- __init__.pyc
`-- EGG-INFO
    |-- dependency_links.txt
    |-- PKG-INFO
    |-- SOURCES.txt
    |-- top_level.txt
    `-- zip-safe
```

打开python终端或者ipython都行，直接导入我们的包

``` Bash
>>> import demo
>>> demo.test()
hello world!
>>>
```
好了，执行成功！

### 进阶

在上例中，我们基本都使用setup()的默认参数，这只能写一些简单的egg。一旦我们的project逐渐变大以后，维护起来就有点复杂了，下面是setup()的其他参数，我们可以学习一下

#### 使用find_packages()

对于简单工程来说，手动增加packages参数很容易，刚刚我们用到了这个函数，它默认在和setup.py同一目录下搜索各个含有__init__.py的包。其实我们可以将包统一放在一个src目录中，另外，这个包内可能还有aaa.txt文件和data数据文件夹。

``` Bash
demo
├── setup.py
└── src
    └── demo
        ├── __init__.py
        ├── aaa.txt
        └── data
            ├── abc.dat
            └── abcd.dat
```

如果不加控制，则setuptools只会将__init__.py加入到egg中，想要将这些文件都添加，需要修改setup.py

``` Python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
        name='demo',
        version="0.1",
        packages=find_packages('src'),  # 包含所有src中的包
        package_dir = {'': 'src'},  # 告诉distutils包都在src下

        # include_package_data = True,
        package_data = {
            # 任何包中含有.txt文件，都包含它
            '': ['*.txt'],
            # 包含demo包data文件夹中的 *.dat文件
            'demo': ['data/*.dat'],
        }
)
```

这样，在生成的egg中就包含了所需文件了。看看：

``` Bash
unzip -l dist/demo-0.1-py2.7.egg

Archive:  dist/demo-0.1-py2.7.egg
  Length     Date   Time    Name
 --------    ----   ----    ----
      122  01-15-16 11:32   demo/__init__.py
      356  01-15-16 13:53   demo/__init__.pyc
        1  01-15-16 13:47   demo/aaa.txt
        1  01-15-16 13:47   demo/data/abc.dat
        1  01-15-16 13:47   demo/data/abcd.dat
        1  01-15-16 13:53   EGG-INFO/dependency_links.txt
      176  01-15-16 13:53   EGG-INFO/PKG-INFO
      157  01-15-16 13:53   EGG-INFO/SOURCES.txt
        5  01-15-16 13:53   EGG-INFO/top_level.txt
        1  01-15-16 13:53   EGG-INFO/zip-safe
 --------                   -------
      821                   10 files
```

另外，也可以排除一些特定的包，如果在src中再增加一个tests包，可以通过exclude来排除它,

``` Python
find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])
```

#### 使用entry_points

一个字典，从entry point组名映射道一个表示entry point的字符串或字符串列表。

Entry points是用来支持动态发现服务和插件的，也用来支持自动生成脚本。

这个还是看例子比较好理解：

``` Python
setup(
    entry_points = {
        'console_scripts': [
            'foo = demo:test',
            'bar = demo:test',
        ],
        'gui_scripts': [
            'baz = demo:test',
        ]
    }
)
```

修改setup.py增加以上内容以后，再次安装这个egg，可以发现在安装信息里头多了两行代码（Linux下）：

``` Bash
Installing foo script to /usr/local/bin
Installing bar script to /usr/local/bin
```

查看/usr/local/bin/foo内容

```console
#!/usr/bin/python
# EASY-INSTALL-ENTRY-SCRIPT: 'demo==0.1','console_scripts','foo'
__requires__ = 'demo==0.1'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('demo==0.1', 'console_scripts', 'foo')()
    )
```

这个内容其实显示的意思是，foo将执行console_scripts中定义的foo所代表的函数。执行foo，发现打出了hello world!，和预期结果一样。

这里其实就是增加一些工具的命令行。

#### 使用Eggsecutable Scripts

从字面上来理解这个词，Eggsecutable是Eggs和executable合成词，翻译过来就是另eggs可执行。也就是说定义好一个参数以后，可以另你生成的.egg文件可以被直接执行，类似Java打包时，manifest里的mainClass。

``` Python
setup(
    # other arguments here...
    entry_points = {
        'setuptools.installation': [
            'eggsecutable = demo:test',
        ]
    }
)
```

这么写意味着在执行python *.egg时，会执行我的test()函数，在文档中说需要将.egg放到PATH路径中。

#### 包含数据文件

在前面我们已经列举了如何包含数据文件，其实setuptools提供的不只这么一种方法，下面是另外两种

1. 包含所有包内文件

    这种方法中包内所有文件指的是受版本控制（CVS/SVN/GIT等）的文件，或者通过MANIFEST.in声明的

    ``` Python
    from setuptools import setup, find_packages
    setup(
        ...
        include_package_data = True
    )
    ```

2. 包含一部分，排除一部分

    ``` Python
    from setuptools import setup, find_packages
    setup(
        ...
        packages = find_packages('src'),  
        package_dir = {'':'src'},   
    
        include_package_data = True,    
    
        # 排除所有 README.txt
        exclude_package_data = { '': ['README.txt'] },
    )
    ```

    如果没有使用版本控制的话，可以还是使用3中提到的包含方法

3. 可扩展的框架和应用

    setuptools可以帮助你将应用变成插件模式，供别的应用使用。官网举例是一个帮助博客更改输出类型的插件，一个博客可能想要输出不同  类型的文章，但是总自己写输出格式化代码太繁琐，可以借助一个已经写好的应用，在编写博客程序的时候动态调用其中的代码。
    
    通过entry_points可以定义一系列接口，供别的应用或者自己调用，例如：
    
    ``` Python
    setup(
        entry_points = {'blogtool.parsers': '.rst = some_module:SomeClass'}
    )
    
    setup(
        entry_points = {'blogtool.parsers': ['.rst = some_module:a_func']}
    )
    
    setup(
        entry_points = """
            [blogtool.parsers]
            .rst = some.nested.module:SomeClass.some_classmethod [reST]
        """,
        extras_require = dict(reST = "Docutils>=0.3.5")
    )
    ```
    
上面列举了三中定义方式，即我们将我们some_module中的函数，以名字为blogtool。

parsers的借口共享给别的应用。别的应用使用的方法是通过pkg_resources.require()来导入这些模块。

另外，一个名叫stevedore的库将这个方式做了封装，更加方便进行应用的扩展。


参考

__[setuptools官方文档](http://pythonhosted.org/setuptools/setuptools.html)__
__[引用的原文](http://yansu.org/2013/06/07/learn-python-setuptools-in-detail.html)__