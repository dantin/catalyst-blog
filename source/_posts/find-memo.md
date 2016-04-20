title: Find备忘录
date: 2016-04-20 11:44:04
categories: 效率
tags: Linux
toc: true
---

本文记录find命令的常见用法。

### 搜目录下包含关键字的文件

```bash
find . -name '*.py' -print0 | xargs -0 grep 'something'
# or
find . -name '*.py' -exec grep 'something' {} \;
```
