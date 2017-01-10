+++
date = "2016-02-02T13:22:29+08:00"
title = "Supervisord备忘录"
categories = ["Engineering"]
tags = ["System", "Memo"]
description = "本文系统后台监控工具，Supervisord"
slug = "system-supervisord"
+++

Supervisor是一个Python开发的client/server系统，可以管理和监控Linux/Unix上面的进程。不过同daemontools一样，它也不能监控daemon进程。

### 组件

Supervisor有不同的部件组成，部件分别负责不同的功能，对进程进行监控和管理。

* supervisord \
  Supervisor的server部分称为supervisord。主要负责管理子进程，响应客户端的命令，log子进程的输出，创建和处理不同的事件
* supervisorctl \
  Supervisor的命令行客户端。它可以与不同的supervisord进程进行通信，获取子进程信息，管理子进程
* Web Server \
  Supervisor的web server，用户可以通过web对子进程进行监控，管理等等，作用与supervisorctl一致。

* XML-RPC interface \
  XML-RPC接口，提供XML-RPC服务来对子进程进行管理，监控

### 安装

安装supervisor很简单，通过pip就可以安装

```console
sudo pip install supervisor
```

安装完成之后，就可以用`echo_supervisord_conf`命令来生成配置文件，例如

```console
echo_supervisord_conf > /etc/supervisord.conf  
echo_supervisord_conf > /path/to/supervisord.conf
```

当然，对于CentOS来说，也能直接通过`yum`命令安装。

```console
yum info supervisor
```

### 配置

配置文件supervisord.conf是一个ini文件，可以对http_server、supervisord、supervisorctl和program进行配置。不过默认生成的文件已经对大部分进行配置，如果简单使用，只需要配置program的部分就可以了。

配置文件必须要有一个program配置项，这样supervisord才知道哪个program需要被管理和监控。例如下面pypi-server应用的配置

```console
[program:pypi-server]
command=/home/sem/venv/pypiserver/bin/pypi-server -p 50001 -P /home/sem/htpasswd.txt /home/sem/pypi_packages
priority=1
numprocs=1
autostart=true
autorestart=true
startretries=10
stopsignal=KILL
stopwaitsecs=10
redirect_stderr=true
stdout_logfile=/var/log/pypi-server/pypi-server.log
```

### 启动

配置文件生成之后，就可以启动supervisord了

```console
supervisord     #默认使用/etc/supervisord.conf的配置文件
supervisord -c /path/to/supervisord.conf
```

或者`/etc/init.d/`中的启动脚本

```console
#!/bin/bash
#
#supervisord   Startup script for the Supervisor process control system
#
# chkconfig:    345 83 04
# description: Supervisor is a client/server system that allows \
#   its users to monitor and control a number of processes on \
#   UNIX-like operating systems.
# processname: supervisord
# config: /etc/supervisord.conf
# config: /etc/sysconfig/supervisord
# pidfile: /var/run/supervisord.pid
#
### BEGIN INIT INFO
# Provides: supervisord
# Required-Start: $all
# Required-Stop: $all
# Short-Description: start and stop Supervisor process control system
# Description: Supervisor is a client/server system that allows
#   its users to monitor and control a number of processes on
#   UNIX-like operating systems.
### END INIT INFO

# Source function library
. /etc/rc.d/init.d/functions

# Source system settings
if [ -f /etc/sysconfig/supervisord ]; then
    . /etc/sysconfig/supervisord
fi

# Path to the supervisorctl script, server binary,
# and short-form for messages.
supervisorctl=/bin/supervisorctl
supervisord=/bin/supervisord
prog=supervisord
pidfile=/var/run/supervisord.pid
lockfile=/var/lock/subsys/supervisord
STOP_TIMEOUT=300
OPTIONS="--c /etc/supervisord.conf"
RETVAL=0

start() {
    echo -n $"Starting $prog: "
    daemon --pidfile=${pidfile} $supervisord $OPTIONS
    RETVAL=$?
    echo
    if [ $RETVAL -eq 0 ]; then
        touch ${lockfile}
        $supervisorctl $OPTIONS status
    fi
    return $RETVAL
}

stop() {
    echo -n $"Stopping $prog: "
    killproc -p ${pidfile} -d ${STOP_TIMEOUT} $supervisord
    RETVAL=$?
    echo
    [ $RETVAL -eq 0 ] && rm -rf ${lockfile} ${pidfile}
}

reload() {
    echo -n $"Reloading $prog: "
    LSB=1 killproc -p $pidfile $supervisord -HUP
    RETVAL=$?
    echo
    if [ $RETVAL -eq 7 ]; then
        failure $"$prog reload"
    else
        $supervisorctl $OPTIONS status
    fi
}

restart() {
    stop
    start
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    status)
        status -p ${pidfile} $supervisord
        RETVAL=$?
        [ $RETVAL -eq 0 ] && $supervisorctl $OPTIONS status
        ;;
    restart)
        restart
        ;;
    condrestart|try-restart)
        if status -p ${pidfile} $supervisord >&/dev/null; then
          stop
          start
        fi
        ;;
    force-reload|reload)
        reload
        ;;
    *)
        echo $"Usage: $prog {start|stop|restart|condrestart|try-restart|force-reload|reload}"
        RETVAL=2
esac

exit $RETVAL
```

### 管理

#### supervisordctl

通过supervisorctl就可以监控管理program。

* supervisorctl stop programxxx \
  停止某一个进程（programxxx），programxxx为"配置文件"里配置的值，这个示例就是chatdemon。
* supervisorctl start programxxx \
  启动某个进程
* supervisorctl restart programxxx \
  重启某个进程
* supervisorctl stop groupworker: \
  重启所有属于名为groupworker这个分组的进程(start,restart同理)
* supervisorctl stop all \
  停止全部进程，注：start、restart、stop都不会载入最新的配置文件。
* supervisorctl reload \
  载入最新的配置文件，停止原有进程并按新的配置启动、管理所有进程。
* supervisorctl update \
  根据最新的配置文件，启动新配置或有改动的进程，配置没有改动的进程不会受影响而重启。

注意：__显示用stop停止掉的进程，用reload或者update都不会自动重启。__

``` console
$ supervisorctl -c conf/app.conf  status
node_app                         RUNNING    pid 6916, uptime 0:00:00
tornado_app                      RUNNING    pid 6917, uptime 0:00:00

$ supervisorctl -c conf/app.conf  stop node_app
node_app: stopped

$ supervisorctl -c conf/app.conf  stop tornado_app
tornado_app: stopped

$ supervisorctl -c conf/app.conf  status
node_app                         STOPPED    Apr 04 02:34 AM
tornado_app                      STOPPED    Apr 04 02:35 AM

$ supervisorctl -c conf/app.conf  start all
node_app: started
tornado_app: started

$ supervisorctl -c conf/app.conf  status
node_app                         RUNNING    pid 8080, uptime 0:00:00
tornado_app                      RUNNING    pid 8079, uptime 0:00:00
```

#### web

如果配置文件开启http server，那么就可以通过web界面来管理program了。

```bash
$ grep -A 3 "inet_http_server" conf/app.conf 
[inet_http_server]         ; inet (TCP) server disabled by default
port=0.0.0.0:8383        ; (ip_address:port specifier, *:port for all iface)
#username=user              ; (default is no username (open server))
#password=123               ; (default is no password (open server))
```

然后打开[http://domain.com:8383](http://domain.com:8383)就可以使用后台访问控制

### 问题

通过supervisord可以很方便的管理program，可以同时管理多个program，也可以管理一个program的多个进程。而且提供了命令行、web、xml-rpc的接口来管理和监控进程，通过配置文件，可以指定进程挂掉后如何处理(可以重启或者其它方式处理挂掉的进程)

但是，supervisord本身也是一个program，如果它自己挂掉没有办法处理！

参考

__[supervisord官方文档](http://supervisord.org/index.html)__