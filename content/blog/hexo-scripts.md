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

### Hexo换Hugo

备注：部分内容还需手动

```python
#coding:utf-8
import os
import re

target_dir = '$HUGO_ROOT/conent/blog'
tag_line = '---\n'
if __name__ == "__main__":
    files = os.listdir(target_dir)
    for i in xrange(len(files)):
        fname = target_dir + '/' + files[i]
        if '.md' not in files[i]:
            continue
        if files[i] in ['_spark-quick-start.md']:
            continue
        # print fname
        lines = []
        header = []

        # read old file content
        tag_count = 0
        desc = ''
        is_target = False
        with open(fname, 'r') as fp:
            for line in fp:
                if line == tag_line:
                    tag_count += 1
                    is_target = True
                    continue
                if tag_count >= 2:
                    if re.match(r"Leetcode \d*", line):
                        desc = line
                    lines.append(line)
                else:
                    header.append(line)

        if not is_target:
            continue
        d = dict(s.strip().split(': ') for s in header)
        tag = ''
        if '[' in d['tags']:
            t = d['tags'][1:-1]
            tag = ', '.join('"{0}"'.format(s.strip()) for s in t.split(','))
        else:
            tag = '"{0}"'.format(d['tags'])

        cat = ''
        if d['categories'] == '练习':
            cat = 'Code'
        elif d['categories'] == '学术':
            cat = 'Scholar'
        elif d['categories'] == '工程':
            cat = 'Engineering'
        elif d['categories'] == '生活':
            cat = 'Life'
        else:
            cat = 'Misc'

        # write file content
        with open(fname, 'w') as fp:
            fp.write('+++\n')
            fp.write('date = "%s"\n' % (d['date'].replace(' ', 'T') + '+08:00'))
            fp.write('title = "%s"\n' % d['title'])
            fp.write('categories = ["%s"]\n' % cat)
            fp.write('tags = ["%s"]\n' % tag)
            fp.write('description = "%s"\n' % desc.strip())
            fp.write('slug = "%s"\n' % files[i].split('.')[0])
            fp.write('+++\n\n')
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
