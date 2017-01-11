#coding:utf-8
import os
import re

target_dir = '/Users/david/Documents/temp/catalyst-posts'
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
        # print files[i]
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

        # print 'date = "%s"' % (d['date'].replace(' ', 'T') + '+08:00')
        # print 'title = "%s"' % d['title']
        # print 'categories = ["%s"]' % cat
        # print 'tags = [%s]' % tag
        # print 'description = "%s"' % desc.strip()
        # print 'slug = "%s"' % files[i].split('.')[0]

        # # write file content
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