---
title: Python Primer
date: 2016-02-06 23:10:37
categories: 工程
tags: Python
toc: true
---

本文记录Python基础的读书笔记。

### Overview

#### Virtualenv

安装Python3

``` bash
virtualenv -p python3 envname
```

更新过程中碰到如下异常：

```
DEPRECATION: The default format will switch to columns in the future. You can use --format=(legacy|columns) (or define a format=(legacy|columns) in your pip.conf under the [list] section) to disable this warning.
```

在`VENV/pip.conf`中添加：

```
[list]
format=columns
```


#### The Python Interpreter

Python是一门解释型语言，它的源代码(Source Code）又称为脚本（Script），即`.py`文件，由`Python Interpreter`负责解释并执行。

``` bash
# 直接运行
python demo.py
# 交互式运行
python -i demo.py
```

Python的语法严重依赖whitespace，它用whitespace表示代码逻辑（if, else/while/for...）和语义结构（函数、类等等）。

### Object in Python

同时，Python又是一门面向对象的语言，'类（classes）'组成了Python的底层数据类型。

常见的Python对象有以下几种：

| classes | 类型      |
| ------- |:--------:|
| int     | 整型      |
| float   | 浮点型    |
| str     | 字符串型  |

#### Identifiers, Objects, and the Assignment Statement

最常见的Python语句是赋值语句，_assignment statement_。

```python
temperature = 98.6
```

__标识符__

这条语句产生一个'标识符'，_identifier_: temperature

> 标识符
> 
> 大小写敏感，包含：字母、数字、下划线，不能用保留字（if, else, True...）

和Java类似，一个标识符指向一个特定内存地址，即，memery address。

但Python是动态类型语言，一个标识符可以指向任意类型的对象，也可以随时更改它所指向的对象类型。不过，虽然一个标识符没有类型，但它指向的对象却拥有类型。

不同的标识符可同时指向同一个对象，这有些类似'别名，_alias_'的概念，一旦别名的指向创建完毕，那么无论通过哪个别名，都能找到那个特定的对象。如：

```python
original = temperature
```

这时，对其中一个别名的操作（修改），另一个别名也能'看见'。

但若其中一个别名的指向改变，上述概念将失效。

```python
temperature = temperature + 5.0
```

因为，此时不同别名指向的对象已经不再一样。

#### Creating and Using Objects

__实例化__

实例化是创建一个对象实例的过程，一般通过构造函数完成。如：

```python
w = Widget()  # without parameters
w = Widget(a, b)  # with parameter
```

Python自带的类也支持常量实例化。如：

```python
temperature = 98.6
```

它创建了一个_float_类型对象。

如果一个函数返回一个对象，那么也能间接通过函数调用实例化对象。如：

```python
l = sorted((4, 1, 2, 3))
```

__方法调用__

Python支持传统的函数`sorted(data)`，也支持方法调用`string.lower()`。

对于方法调用，需要区别：

* _accessors_，返回对象内部数据，不改变对象状态
* _mutators_或_update methods_，改变对象状态

#### Python's Build-In Classes

Python自带对象如下表

| classes   | 描述     | Immutable? |
| --------- | ------- |:-----------:|
| bool      | 布尔型   | Y |
| int       | 整型     | Y |
| float     | 浮点型   | Y |
| list      | 列表     |   |
| tuple     | 元组     | Y |
| str       | 字符串型 | Y |
| set       | 集合    |   |
| frozenset | 集合    | Y |
| dict      | 字典    |   |

需要特别注意：

* _mutable_，可变对象，可通过方法改变对象内部数据
* _immutable_，不可变对象，只能通过标识符重新指向新对象

__The bool class__

逻辑_True_，_False_

构造函数：bool(foo)

类型转换：bool(int), bool(float), bool(set)...

__The int class__

只有一种精度

支持二进制、八进制、十进制：_0b1011_, _0o52_, _0x7f_

构造函数：int()

类型转换：int(f), int(s), _ValueError_异常

不同基数的转换：`int('7f', 16)`

__The float class__

同样也只有一种精度，支持科学计数法：_6.022e23_

类型转换：float(i), float(s), _ValueError_异常

__The list class__



### Expressions, Operators, and Precedence



### Control Flow

### Functions

### Simple Input and Output

### Exception Handling

### Iterators and Generators