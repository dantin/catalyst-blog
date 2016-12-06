# -*- coding: utf-8 -*-
"""Fabric build scripts
"""
from fabric.api import *

# The main module name, which is equal to repository name
env.name = 'catalyst'
# Git repository url
env.repository = 'git@github.com:dantin/catalyst-blog.git'
# Default Git branch
env.branch = 'master'
env.path = '/usr/local/var/www/%s' % env.name

# Custom settings for different environments
# path：项目部署目录
env.settings = {
    # 线上环境
    'prod': {
        'tier': 'prod',
        'hosts': ['dding-prod:29000'],
        'user': 'dding',
        'password': '',
        'path': '/var/www/%s' % env.name,
        'activate': '/home/dding/Documents/venv/devops/bin/activate',
        'src': '/home/dding/Documents/code/%s' % env.name
    },
    # 本地开发环境
    'local': {
        'tier': 'local',
        'hosts': ['127.0.0.1:22'],
        'user': 'david',
        'password': '',
        'path': '/usr/local/var/www/%s' % env.name,
        'activate': '/home/sem/venv/devops/',
        'src': '/Users/david/Documents/code/cosmos/%s' % env.name
    }
}

env.hosts = ['']
env.src = ''
env.tier = 'local'

def tier(tier='local'):
    """environment setting
    """
    env.update(env.settings[tier])

def fetch():
    """
    Git fetch
    """
    with(cd(env.src)):
        local("git fetch")


def update():
    """
    Git update src files
    """
    with(cd(env.src)):
        local('git pull')


def checkout(branch=None):
    """
    Git checkout to branch
    :param branch: target branch
    """
    """
    :param branch:
    :return:
    """
    if not branch:
        branch = env.branch
    with(cd(env.src)):
        local('git checkout %s' % branch)


def build(branch='master'):
    fetch()
    checkout(branch)
    update()


def publish():
    local('hexo generate')
    local('tar -czf %s.tar.gz -C public .' % env.name)


def deploy():
    if(env.tier == 'prod'):
        run('sudo tar zxf %s/%s.tar.gz -C %s' % (env.src, env.name, env.path))
    else:
        local('tar zxf %s.tar.gz -C %s' % (env.name, env.path))


def clean():
    local('rm -rf public/*')
    local('rm -rf %s/*' % env.path)
