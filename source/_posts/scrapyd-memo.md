title: Scrapyd备忘录
date: 2016-01-08 10:33:37
categories: 学习
tags: Scrapyd
toc: true
---

[Scrapyd](http://scrapyd.readthedocs.org/en/latest/index.html)是一套管理scrapy类爬虫的框架，支持多项目、多版本。在爬虫有多版本时，只有最新版本的爬虫有效。

### 运行机制

Scrapyd通常作为一个daemon进程运行在后台，侦听请求，并开启进程运行爬虫进程：

``` Bash
scrapy crawl myspider
```

Scrapyd在内部并行运行在多CPU上，并使用__max_proc__和__max_proc_per_cpu__选项控制并发量。

Scrapyd使用[Twisted Application Framework](http://twistedmatrix.com/documents/current/core/howto/application.html)对外提供REST接口，用eggs管理爬虫版本，以插件形式支持自定义相关模块。

### 安装

依赖包安装

``` Bash
pip install scrapyd
```

启动

``` Bash
scrapyd
```

#### 服务化

通常情况下会把Scrapyd配置为Daemon服务。

启动脚本：/etc/init.d/scrapyd

``` Bash
#!/bin/bash
#
# scrapyd      This shell script enables scrapyd server on boot
#
# chkconfig:   - 50 01
#
# description: Autostart scrapyd web scraper framework daemon
# processname: scrapyd
#

# source function library
. /etc/rc.d/init.d/functions

RETVAL=0

PID='/var/run/scrapyd.pid'
VIRTUALENV='/home/sem/venv/scrapyd/bin/activate'
OPTIONS='--pidfile='${PID}

start() {
        source ${VIRTUALENV}
        if [ -f ${PID} ]; then
                echo -n "Scrapy already running."
                RETVAL=0
        else
                echo -n "Attempting to start scrapyd service... "
                scrapyd ${OPTIONS} &
                RETVAL=$?
        fi
        echo
}

stop() {
        source ${VIRTUALENV}
        if [ -f ${PID} ]; then
                echo -n "Attempting to stop scrapyd service... "
                kill `cat $PID`
                RETVAL=$?
        else
                echo -n "Scrapyd not running"
                RETVAL=0
        fi
        echo
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
  restart|force-reload)
        restart
        ;;
  reload)
        ;;
  status)
        if [ -f $PID ]; then
                echo "Scrapyd is running."
                RETVAL=0
        else
                echo "Scrapyd is not running."
                RETVAL=3
        fi
        ;;
  *)
        echo "Usage: $0 {start|stop|status|restart|reload|force-reload}"
        exit 1
esac

exit ${RETVAL}
```

配置文件

__/etc/scrapydscrapyd.conf__

``` Bash
[scrapyd]
eggs_dir    = /adeaz/sem/semdata/app/scrapyd/eggs
logs_dir    = /adeaz/sem/semdata/app/scrapyd/logs
items_dir   = /adeaz/sem/semdata/app/scrapyd/items
jobs_to_keep = 5
dbs_dir     = /adeaz/sem/semdata/app/scrapyd/dbs
max_proc    = 0
max_proc_per_cpu = 4
finished_to_keep = 100
poll_interval = 5
http_port   = 6800
debug       = off
runner      = scrapyd.runner
application = scrapyd.app.application
launcher    = scrapyd.launcher.Launcher
webroot     = scrapyd.website.Root

[services]
schedule.json     = scrapyd.webservice.Schedule
cancel.json       = scrapyd.webservice.Cancel
addversion.json   = scrapyd.webservice.AddVersion
listprojects.json = scrapyd.webservice.ListProjects
listversions.json = scrapyd.webservice.ListVersions
listspiders.json  = scrapyd.webservice.ListSpiders
delproject.json   = scrapyd.webservice.DeleteProject
delversion.json   = scrapyd.webservice.DeleteVersion
listjobs.json     = scrapyd.webservice.ListJobs
#daemonstatus.json = scrapyd.webservice.DaemonStatus
```

### 爬虫项目准备

为了让Scrapy项目可以被Scrapyd管理，需要单独编写setup.py文件，提供eggs。

例子：

``` Python
# used by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
        name='composer_crawlers',
        version='1.0',
        packages=find_packages(),
        entry_points={'scrapy': ['settings = crawlers.settings']},
)
```

在scrapy.cfg中根据环境修改deploy配置

``` Bash
[deploy:dev]
url = http://10.3.1.241:6800/
project = composer
```

部署爬虫到DEV环境。

``` Bash
scrapyd-deploy dev -p composer
```

### 常用操作

``` Bash
# 项目列表
curl http://10.3.1.241:6800/listprojects.json
# 项目爬虫列表
curl http://10.3.1.241:6800/listspiders.json\?project\=composer
# 远程运行composer的google_search爬虫
curl http://10.3.1.241:6800/schedule.json -d project=composer -d spider=google_search -d query=Test
# daemon状态
curl http://10.3.1.241::6800/daemonstatus.json
# 删除一个项目
curl http://10.3.1.241:6800/delproject.json -d project=composer
# 爬虫版本
curl http://10.3.1.241:6800/listversions.json\?project\=composer
# 版本回退
curl http://10.3.1.241:6800/delversion.json -d project=composer -d version=1452134448
```
