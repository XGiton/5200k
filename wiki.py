#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import sys

import api
import model


wiki_dir = sys.path[0] + '/wiki/'

# Clone or pull.
if os.path.exists(wiki_dir):
    p = subprocess.Popen('git pull origin master', cwd=wiki_dir, shell=True)
else:
    sh = 'mkdir wiki && cd wiki && git init &&  git remote add origin\
        git@github.com:XGiton/base_project.wiki.git'
    p = subprocess.Popen(sh, cwd=sys.path[0], shell=True)
p.wait()


def make_api_page(filename, func_list):
    with open(wiki_dir + '.'.join([filename, 'markdown']), 'w') as f:
        # add error code
        f.write('### Error Code\n')
        for i, fc in enumerate(func_list):
            if fc.__name__ == 'Error':
                dic = {}
                for k, v in fc.__dict__.items():
                    if k[0] != '_':
                        dic[k] = v
                # write into files
                values = list(dic.values())
                values.sort(key=lambda x: x['err'])
                for v in values:
                    line = '* `%d`: %s\n' % (v['err'], v['msg'])
                    f.write(line)
                func_list.pop(i)

        f.write('\n---\n')

        # add link
        f.write('### Api Link\n')

        def get_link(index, func):
            title = func.__doc__.splitlines()[1]
            title = title.split('#')[-1].strip()
            title = 'API-%d %s' % (index + 1, title)

            def deal(string):
                string = string.lower().replace(' ', '-')
                s = []
                for a in string:
                    if a in '1234567890abcdefghijklmnopqrstuvwxyz-':
                        s.append(a)
                if s[-1] == '-':
                    s.pop(-1)
                return "".join(s)
            return '* [%s](#%s)\n' % (title, deal(title))

        for ind, fun in enumerate(func_list):
            f.writelines(get_link(ind, fun))

        # if app title
        # add api No
        def is_head(title):
            if title is not None and len(title) > 6 and title[4:7] == '## ':
                return True
            else:
                return False

        f.write('\n---\n')
        for i, fc in enumerate(func_list):
            f.writelines(map(lambda l: '## API-%d %s\n' % ((i + 1), l[7:])
                             if is_head(l) else l[4:] + '\n',
                             fc.__doc__.splitlines()))


def make_model_page(filename, mod):
    with open(wiki_dir + '.'.join([filename, 'markdown']), 'w') as f:
        # remove first 4 whitespaces
        f.writelines(map(lambda l: '\n' if not l else l[4:] + '\n',
                         mod.__doc__.splitlines()))


wiki_api = {
    'API-User': [
    ],
}


wiki_model = {
    "Model-Setting": model.setting.Setting,
}

# Generate wiki pages for apis.
for page_name, funcs_list in wiki_api.items():
    make_api_page(page_name, funcs_list)

# Generate wiki pages for models.
for page_name, model_class in wiki_model.items():
    make_model_page(page_name, model_class)

# Commit and push.
sh = 'git add -A && git commit -m "Update Wiki" && git push origin master'
p = subprocess.Popen(sh, cwd=wiki_dir, shell=True)
p.wait()
