+++
title = "Curl备忘录"
categories = ["Misc"]
tags = ["Network", "Memo"]
description = "本文记录curl常用方法"
slug = "tools-curl-memo"
date = "2017-01-15T23:21:03+08:00"
+++

### 特殊用法

支持跳转，Redirect：`-L`同`--location`

```console
curl -L http://www.target.com
```