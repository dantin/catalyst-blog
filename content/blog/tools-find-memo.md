+++
date = "2016-04-20T11:44:04+08:00"
title = "Find备忘录"
categories = ["Misc"]
tags = ["Memo", "Linux"]
description = "本文记录find命令的常见用法"
slug = "tools-find-memo"
+++

### 搜目录下包含关键字的文件

```console
find . -name '*.py' -print0 | xargs -0 grep 'something'
# or
find . -name '*.py' -exec grep 'something' {} \;
# ignore directory
find . -name "*.go" -not -path "./_vendor/*" -print0 | xargs -0 grep 'keyword'
```

### 删除目录中除某些子目录外的内容

```console
find $DEPLOY_DIR -not \( -type f -regex '.*/static/*' -prune \) -type f -print0 | xargs -0 rm -f
```

### 删除空目录

```console
find -x /usr/local/var/www/catalyst -type d -empty -print0 | xargs -0 rmdir
```