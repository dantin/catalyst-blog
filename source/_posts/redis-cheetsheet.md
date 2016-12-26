---
title: Redis Cheetsheet
date: 2016-04-11 09:57:43
categories: 工程
tags: [Redis, Cheetsheet]
toc: true
---

本文记录Redis的常用工具。

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