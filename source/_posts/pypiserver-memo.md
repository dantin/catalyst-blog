title: Pypiserver备忘录
date: 2016-01-21 15:24:26
categories: 学习
tags: [PypiServer, Python]
toc: true
---

[Pypiserver](https://pypi.python.org/pypi/pypiserver)是一款类似Java世界里Nexus的软件，可以搭建Python的私有仓库，小规模管理团队内部的一些Python软件包。

### 安装和配置

``` Bash
# 安装
pip install pypiserver
# 创建Python egg的保存目录
mkdir ~/packages
# 启动服务
pypi-server -p 40000 ~/packages & #  默认侦听所有IP

## Download and Install hosted packages.
pip install --extra-index-url http://localhost:40000/simple/ package
```

使用`--extra-index-url`比较麻烦，可以通过配置`~/.pip/pip.conf`避免敲重复代码。

``` Bash
[global]
extra-index-url = http://localhost:40000/simple/
```

### 上传软件包

使用前需要安装passlib包

``` Bash
pip install passlib
```

创建认证用户

``` Bash
htpasswd -sc htpasswd.txt <some_username>

# 重启
./pypi-server -p 40000 -P htpasswd.txt ~/packages &
```

在客户端，需要在`~/.pypirc`输入如下内容：

``` Bash
[distutils]
index-servers =
  pypi
  local

[pypi]
username:<your_pypi_username>
password:<your_pypi_passwd>

[local]
repository: http://localhost:8080
username: <some_username>
password: <some_passwd>
```

然后在Python项目里上传自制的软件包。

``` Bash
python setup.py sdist upload -r local
```

总之，Pypiserver可以解决Python的私有软件仓库的问题，但配置起来较麻烦，具有一定的学习曲线。
