#!/bin/bash

thingscope_root='/var/www/thingscope-backend'
thingscope_public_dir=$thingscope_root/public
thingscope_web_dir=$HOME/thingscope-ui

cd $thingscope_web_dir
git pull origin master
rm -fr node_modules/
rm -fr build
npm install
#npm audit fix
npm run build

cd $thingscope_public_dir
rm -fr static
shopt -s extglob
rm -v !("irt_logo.svg"|"README.md"|"views"|"cs_cu.svg")

cd $thingscope_web_dir/build
cp -r * $thingscope_public_dir
