+++
date = "2017-01-16T15:17:48+08:00"
title = "安装Airflow"
slug = "tools-airflow-installation"
categories = ["Engineering"]
tags = ["Memo", "Tools"]
description = "本文记录Airflow的安装过程"
+++

### 环境准备

添加用户

```console
adduser dding
passwd dding
usermod -aG wheel dding
```

安装`virtualenv`

```console
wget https://bootstrap.pypa.io/ez_setup.py -O - | python
easy_install pip
pip install virtualenv
```

配置虚拟环境

```console
virtualenv venv/airflow
```

### 安装

安装`airflow`

```console
pip install airflow
# Hive Sample的Bug
pip install "airflow[hive]"
# MySQL连接的Bug
pip install "airflow[mysql]"
```

支持登陆

```console
pip install "airflow[password]"
```

### 配置

主要变更内容如下：

* Executor从`SequentialExecutor`变更为`LocalExecutor`
* 禁用示例：`load_examples = False`
* 变更Web端口：`38080`

```console
[core]

...
# The executor class that airflow should use. Choices include
# SequentialExecutor, LocalExecutor, CeleryExecutor
#executor = SequentialExecutor
executor = LocalExecutor

# The SqlAlchemy connection string to the metadata database.
# SqlAlchemy supports many different database engine, more information
# their website
#sql_alchemy_conn = sqlite:////home/user/airflow/airflow.db
sql_alchemy_conn = mysql://username:password@host:port/airflow_db

# Whether to load the examples that ship with Airflow. It's good to
# get started, but you probably want to set this to False in a production
# environment
#load_examples = True
load_examples = False
...

[webserver]
# The base url of your website as airflow cannot guess what domain or
# cname you are using. This is used in automated emails that
# airflow sends to point links to the right web server
base_url = http://10.12.21.145:38080

# The ip specified when starting the web server
web_server_host = 0.0.0.0

# The port on which to run the web server
web_server_port = 38080
...
```

增加登陆验证

```console
# Set to true to turn on authentication:
# http://pythonhosted.org/airflow/installation.html#web-authentication
#authenticate = False
authenticate = True
auth_backend = airflow.contrib.auth.backends.password_auth
```

增加用户

```console
$ cd ~/airflow
$ python
Python 2.7.9 (default, Feb 10 2015, 03:28:08)
Type "help", "copyright", "credits" or "license" for more information.
>>> import airflow
>>> from airflow import models, settings
>>> from airflow.contrib.auth.backends.password_auth import PasswordUser
>>> user = PasswordUser(models.User())
>>> user.username = 'new_user_name'
>>> user.email = 'new_user_email@example.com'
>>> user.password = 'set_the_password'
>>> session = settings.Session()
>>> session.add(user)
>>> session.commit()
>>> session.close()
>>> exit()
```