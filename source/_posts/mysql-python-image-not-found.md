title: MySQL-python中image not found的解决办法
date: 2016-04-06 10:38:24
categories: 工程
tags: [MySQL, Python]
toc: true
---

本文记录升级MySQL后，MySQL-python不能使用的解决办法。

### 现象

升级MySQL 5.7.11后`MySQL-python`不能使用。

```python
>>> import MySQLdb
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/david/Documents/venv/python2/lib/python2.7/site-packages/MySQLdb/__init__.py", line 19, in <module>
    import _mysql
ImportError: dlopen(/Users/david/Documents/venv/python2/lib/python2.7/site-packages/_mysql.so, 2): Library not loaded: /usr/local/lib/libmysqlclient.18.dylib
  Referenced from: /Users/david/Documents/venv/python2/lib/python2.7/site-packages/_mysql.so
  Reason: image not found
```

### 解决办法

查看`_mysql.so`如何定位到`libmysqlclient.18.dylib`。

```bash
otool -L /Users/david/Documents/venv/python2/lib/python2.7/site-packages/_mysql.so
/Users/david/Documents/venv/python2/lib/python2.7/site-packages/_mysql.so:
    /usr/local/lib/libmysqlclient.18.dylib (compatibility version 18.0.0, current version 18.0.0)
    /usr/lib/libssl.0.9.8.dylib (compatibility version 0.9.8, current version 0.9.8)
    /usr/lib/libcrypto.0.9.8.dylib (compatibility version 0.9.8, current version 0.9.8)
    /usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1213.0.0)
```

使用brew安装MySQL 5.7版本的dylib的位置是: `/usr/local/lib/libmysqlclient.20.dylib`。

把dylib换成自己环境的位置。

```bash
sudo install_name_tool -change /usr/local/lib/libmysqlclient.18.dylib /usr/local/lib/libmysqlclient.20.dylib /Users/david/Documents/venv/python2/lib/python2.7/site-packages/_mysql.so
```

再次确认后，`_mysql.so`已经找到`libmysqlclient.20.dylib`。

```bash
otool -L /Users/david/Documents/venv/python2/lib/python2.7/site-packages/_mysql.so
/Users/david/Documents/venv/python2/lib/python2.7/site-packages/_mysql.so:
    /usr/local/lib/libmysqlclient.20.dylib (compatibility version 18.0.0, current version 18.0.0)
    /usr/lib/libssl.0.9.8.dylib (compatibility version 0.9.8, current version 0.9.8)
    /usr/lib/libcrypto.0.9.8.dylib (compatibility version 0.9.8, current version 0.9.8)
    /usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1213.0.0)
```

至此问题解决。

```python
>>> import MySQLdb
>>> import MySQLdb as mysql
>>> conn = mysql.connect( charset="utf8", use_unicode=True, host="localhost",user="fdd_axb", passwd="try1now",db="fdd_axb" )
>>>
```

### 脚本

如果用虚拟环境, 每个环境都需要类似的执行一次, 有点麻烦, 暂时的解决方式是使用脚本(`fix-mysql-python.sh`), shell代码如下:

```bash
PACKAGES_PATH=`python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())"`
echo $PACKAGES_PATH
install_name_tool -change libmysqlclient.18.dylib /usr/local/lib/libmysqlclient.20.dylib $PACKAGES_PATH/_mysql.so
echo "fix MySQL-python finish"
```
参考

[Python mysqldb: Library not loaded: libmysqlclient.18.dylib](http://stackoverflow.com/questions/6383310/python-mysqldb-library-not-loaded-libmysqlclient-18-dylib/13421926#13421926)