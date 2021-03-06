#!/bin/bash

thingscope_root='/var/www/thingscope/backend'
thingscope_public_dir=$thingscope_root/public
thingscope_web_dir=$PWD

cd $thingscope_web_dir
rm -fr node_modules/
rm -fr build
npm install
INLINE_RUNTIME_CHUNK=false npm run build

cd $thingscope_root
mkdir -p public

cd $thingscope_public_dir
rm -fr *

cd $thingscope_web_dir/build
cp -r * $thingscope_public_dir
cd $thingscope_web_dir/public
cp favicon.ico cs_cu.svg irt_logo.svg $thingscope_public_dir
