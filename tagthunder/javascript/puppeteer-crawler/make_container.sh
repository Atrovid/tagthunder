#!/bin/sh

docker build . -t tagthunder-crawler && clear && docker run -p 8080:8080 tagthunder-crawler
