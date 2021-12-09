#!/bin/sh
DIR="$(dirname "$(realpath "$0")")"

cd ../html-augmentation/ && npm pack && mv *.tgz $DIR/node_modules && cd -
npm install
docker build . -t tagthunder-crawler 
