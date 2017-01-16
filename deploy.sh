#!/bin/bash

BUNDLE_NAME="catalyst"
#DEPLOY_DIR="/var/www/$BUNDLE_NAME"
DEPLOY_DIR="/usr/local/var/www/$BUNDLE_NAME"
VENV_DIR="/home/david/Documents/venv/devops"

source $VENV_DIR/bin/activate
cd `dirname $0`
cd ..
cd $BUNDLE_NAME
ROOT_DIR=`pwd`
# update theme
cd $ROOT_DIR/themes/${BUNDLE_NAME}-hugo
git pull
# update content
cd $ROOT_DIR
git pull
rm -rf public
#hexo generate
$GOPATH/bin/hugo --baseURL http://www.dding.info/
tar -czf ${BUNDLE_NAME}.tar.gz -C public .
# remove old files except 'static' directory
#find $DEPLOY_DIR -not \( -type f -regex '.*/static/*.*' -prune \) -type f -print0 | xargs -0 rm -f
# clear empty directory
#find $DEPLOY_DIR -type d -empty -print0 | xargs -0 sudo rmdir
find $DEPLOY_DIR -type f -print0 | xargs -0 rm -f
find $DEPLOY_DIR -type d -empty -print0 | xargs -0 sudo rmdir
sudo tar -zxf ${BUNDLE_NAME}.tar.gz -C $DEPLOY_DIR
# change file permissions
# no need to grant to root:root
# sudo chown -R root:root $DEPLOY_DIR
find $DEPLOY_DIR -type d -print0 | xargs -0 sudo chmod 755
find $DEPLOY_DIR -type f -print0 | xargs -0 sudo chmod 644