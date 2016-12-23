#!/bin/bash

BUNDLE_NAME="catalyst"
DEPLOY_DIR="/var/www/$BUNDLE_NAME/"

cd `dirname $0`
cd ..
cd $BUNDLE_NAME
ROOT_DIR=`pwd`
git pull
hexo generate
tar -czf ${BUNDLE_NAME}.tar.gz -C public .
sudo tar -zxf ${BUNDLE_NAME}.tar.gz -C $DEPLOY_DIR
