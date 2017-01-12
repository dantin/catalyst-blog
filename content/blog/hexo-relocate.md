+++
date = "2016-12-26T23:41:16+08:00"
title = "Hexo搬迁记录"
categories = ["Misc"]
tags = ["Hexo"]
description = "本文简单记录Hexo网站搬迁过程"
slug = "hexo-relocate"
+++

### 创建用户

```console
adduser username
passwd username
```

修改用户权限，CentOS中wheel组的用户默认具有sudo权限。

```console
usermod -aG wheel username
```

### 工具准备

安装Git

```console
sudo yum install git
```

安装基本工具类库和开发包

```console
sudo yum install epel-release
sudo yum groupinstall 'Development Tools'
sudo yum install openssl-devel
```

安装Node和NPM

```console
sudo yum install nodejs
node --version

sudo yum install npm
```

安装Nginx

```console
sudo yum install nginx
```

安装Python相关内容

```console
sudo yum install python-devel
sudo yum install python-pip
sudo pip install virtualenv
```

### 配置

设置Git

```console
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

生成SSH key

```console
ssh-keygen -t rsa -b 4096 -C "bandwagonhost"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
```

_NOTE_: 去github添加SSH key。

服务启动、防火墙配置

```console
sudo systemctl start nginx
sudo systemctl start firewalld.service
sudo firewall-cmd --permanent --zone=public --add-service=http 
sudo firewall-cmd --permanent --zone=public --add-service=https
sudo firewall-cmd --reload
```

配置服务的后台运行

```console
sudo systemctl enable nginx
sudo systemctl enable firewalld
```

其中：

* Web服务器根目录: /usr/share/nginx/html
* Nginx的默认配置: /etc/nginx/conf.d/default.conf
* Virtual Hose配置: /etc/nginx/conf.d/*.conf
* NginX的全局配置: /etc/nginx/nginx.conf

配置Python虚拟环境，安装Fabric

```console
virtualenv devops
source devops/bin/activate
pip install fabric
```

查看公网地址，并验证

```console
ip addr
```

### 服务配置

全局安装hexo

```console
sudo npm install -g hexo
```

下载工程

```console
cd catalyst/
git init .
git remote add origin git@github.com:dantin/catalyst-blog.git
git pull origin master
git branch --set-upstream-to=origin/master master

git reset --hard

npm install hexo-renderer-sass --save
npm install hexo-renderer-jade --save
```

后面就是坚持更新了...

参考：

* [创建用户](https://www.digitalocean.com/community/tutorials/how-to-create-a-sudo-user-on-centos-quickstart)
* [Git安装](https://www.digitalocean.com/community/tutorials/how-to-install-git-on-centos-7)
* [Node安装](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-a-centos-7-server)
* [NginX安装](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-centos-7)
