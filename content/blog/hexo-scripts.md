+++
date = "2016-12-26T16:54:06+08:00"
title = "Hexo脚本"
categories = ["Misc"]
tags = ["Hexo"]
description = "本文记录基于Hexo的一些批量工具脚本"
slug = "hexo-scripts"
+++

### 修改记录头

新旧版本的Hexo模版不匹配。

具体来说，新版头部：

```console
title: title
date: data
categories: category
tags: [tags]
```

而旧版头部缺少第一行的`---`。

```console
title: title
date: data
categories: category
tags: [tags]
```

为了统一风格，撸了个Python脚本，统一处理。

```python
#coding:utf-8

import os

target_dir = '$HEXO_ROOT/source/_posts'
tag_line = '---\n'

if __name__ == "__main__":
    files = os.listdir(target_dir)

    for i in xrange(len(files)):
        fname = target_dir + '/' + files[i]
        lines = []
        first_line = ''
        # read old file content
        with open(fname, 'r') as fp:
            for line in fp:
                if not first_line:
                    first_line = line
                lines.append(line)
        
        if first_line == tag_line:
            continue

        print fname
        # write file content
        with open(fname, 'w') as fp:
            fp.write(tag_line)
            for line in lines:
                fp.write(line)

```

### 更换分类

备注：前提文件前缀有一定的规律。

```python
#coding:utf-8

import os

target_dir = '$HEXO_ROOT/source/_posts'
tag_line = 'leetcode-'

if __name__ == "__main__":
    files = os.listdir(target_dir)

    for i in xrange(len(files)):
        fname = target_dir + '/' + files[i]

        if files[i][:len(tag_line)] != tag_line:
            continue

        print fname

        lines = []
        # read old file content
        with open(fname, 'r') as fp:
            for line in fp:
                lines.append(line)
        
        # write file content
        with open(fname, 'w') as fp:
            for line in lines:
                if line == 'categories: <from category>\n':
                    fp.write('categories: <to category>\n')
                else:
                    fp.write(line)
```
