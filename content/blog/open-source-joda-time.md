+++
date = "2016-04-08T10:36:23+08:00"
title = "时间日期工具库：Joda-Time"
categories = ["Engineering"]
tags = ["Memo", "Open Source"]
description = "本文记录JodaTime包的使用"
slug = "open-source-joda-time"
+++

Joda-Time提供了一组Java类包用于处理包括ISO8601标准在内的Date和Time。可以利用它把JDK Date和Calendar类完全替换掉，而且仍然能够提供很好的集成。本文记录Joda-Time的使用方法。

### 创建任意时间对象

```java
// jdk
Calendar calendar=Calendar.getInstance();
calendar.set(2012, Calendar.NOVEMBER, 15, 18, 23,55);

// joda-time
DateTime dateTime=new DateTime(2012, 12, 15, 18, 23,55);
```

### 计算两日期相差的天数

```java
// jdk
Calendar start = Calendar.getInstance(); 
start.set(2012, Calendar.NOVEMBER, 14);

Calendar end = Calendar.getInstance();
end.set(2012, Calendar.NOVEMBER, 15);

long startTim = start.getTimeInMillis();
long endTim = end.getTimeInMillis();
long diff = endTim-startTim;

int days=(int) (diff/1000 / 3600 / 24);

// joda-time
LocalDate start=new LocalDate(2012, 12,14);
LocalDate end=new LocalDate(2012, 12, 15);
int days = Days.daysBetween(start, end).getDays();
```

### 时间格式化

```java
DateTimeFormatter format = DateTimeFormat.forPattern("yyyy-MM-dd HH:mm:ss");

//时间解析
DateTime dateTime = DateTime.parse("2012-12-21 23:22:45", format);

//时间格式化，输出==> 2012/12/21 23:22:45 Fri
String string_u = dateTime.toString("yyyy/MM/dd HH:mm:ss EE");
System.out.println(string_u);

//格式化带Locale，输出==> 2012年12月21日 23:22:45 星期五
String string_c = dateTime.toString("yyyy年MM月dd日 HH:mm:ss EE",Locale.CHINESE);
System.out.println(string_c);
```

### 与JDK互操作

```java
//通过jdk时间对象构造
Date date = new Date();
DateTime dateTime = new DateTime(date);

Calendar calendar = Calendar.getInstance();
dateTime = new DateTime(calendar);

// Joda-time 各种操作.....
dateTime = dateTime.plusDays(1) // 增加天
                    .plusYears(1)// 增加年
                    .plusMonths(1)// 增加月
                    .plusWeeks(1)// 增加星期
                    .minusMillis(1)// 减分钟
                    .minusHours(1)// 减小时
                    .minusSeconds(1);// 减秒数

// 计算完转换成jdk 对象
Date date2 = dateTime.toDate();
Calendar calendar2 = dateTime.toCalendar(Locale.CHINA);
```

参考

[Joda-Time官网](http://www.joda.org/joda-time/index.html)