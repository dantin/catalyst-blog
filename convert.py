#coding:utf-8
import os
import re

target_dir = '/Users/david/Documents/code/cosmos/catalyst2/content/blog'
tag_line = '---\n'
if __name__ == "__main__":
    files = os.listdir(target_dir)
    for i in xrange(len(files)):
        fname = target_dir + '/' + files[i]
        if '.md' not in files[i]:
            continue
        if files[i] in ['leetcode-zigzag-conversion.md', 'leetcode-4sum-ii.md', 'leetcode-word-pattern.md', 'leetcode-valid-sudoku.md',
                        'leetcode-longest-repeating-character-replacement.md', 'leetcode-decode-string.md']:
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
        if '[' in d['categories']:
            print fname
            continue
        if '[' in d['tags']:
            print fname
            continue

        cat = ''
        if d['categories'] == '练习':
            cat = 'Code'
        # write file content
        with open(fname, 'w') as fp:
            fp.write('+++\n')
            fp.write('date = "%s"\n' % (d['date'].replace(' ', 'T') + '+08:00'))
            fp.write('title = "%s"\n' % d['title'])
            fp.write('categories = ["%s"]\n' % cat)
            fp.write('tags = ["%s"]\n' % d['tags'])
            fp.write('description = "%s"\n' % desc.strip())
            fp.write('slug = "%s"\n' % files[i].split('.')[0])
            fp.write('+++\n\n')
            for line in lines:
                fp.write(line)