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
env.path = '/var/www/%s' % env.name

# Custom settings for different environments
# path：项目部署目录
env.settings = {
    # 线上环境
    'prod': {
        'tier': 'prod',
        'hosts': ['52.8.242.143:22'],
        'user': 'sem',
        'password': '',
        # 'key_filename': '~/.ssh/id_rsa',
        'path': '/adeaz/sem/app/%s' % env.name,
        'activate': '/home/sem/.VENV27/bin/activate',
        'src': '/adeaz/sem/semcode/%s' % env.name
    },
    # 本地开发环境
    'local': {
        'tier': 'local',
        'hosts': ['127.0.0.1:22'],
        'user': 'sem',
        'password': '',
        'path': '/Users/david/Documents/www/%s' % env.name,
        'activate': '/home/sem/venv/airflow/',
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
    local('tar -cf %s.tar.gz -C public .' % env.name)


def deploy():
    local('tar zxf %s.tar.gz -C %s' % (env.name, env.path))


def clean():
    local('rm -rf public/*')
    local('rm -rf %s/*' % env.path)
