+++
date = "2016-04-11T09:57:43+08:00"
title = "Redis备忘录"
categories = ["Engineering"]
tags = ["Redis", "Memo"]
description = "本文记录Redis的常用命令"
slug = "redis-memo"
+++

### 状态监控

#### INFO

INFO命令可以查看Redis信息和状态。

详细指标参见[链接](http://redisdoc.com/server/info.html)。

```bash
127.0.0.1:6379> info
# Server
redis_version:3.0.7
redis_git_sha1:00000000
redis_git_dirty:0
redis_build_id:ca156bbb7812e807
redis_mode:standalone
```