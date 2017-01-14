+++
date = "2016-08-10T14:20:21+08:00"
title = "Java Object的基本方法"
categories = ["Engineering"]
tags = ["Java"]
description = "本文记录Java Object的基本方法"
slug = "java-object"
+++

### 等待通知相关

| 方法名称         | 描述      |
| --------------- | -------- |
| notify()        | 通知一个在对象上等待的线程，使其从wait()方法返回，而返回的前提是该线程获取到了对象的锁 |
| notifyAll()     | 通知所有等待在该对象上的线程 |
| wait()          | 调用该方法的线程进入WAITING状态，只有等待另外线程的通知或被中断才会返回，需要注意，调用wait()方法后，会释放对象的锁 |
| wait(long)      | 超时等待一段时间，这里的参数时间是毫秒，也就是等待长达n毫秒，如果没有通知就超时返回 |
| wait(long, int) | 对于超时时间更细粒度的控制，可以达到纳秒 |