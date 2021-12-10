#!/bin/bash

yellow=`tput setaf 3`;
green=`tput setaf 2`;
clear=`tput sgr0`;

echo "${yellow}Install python3.9, docker, node.js${clear}"
sudo apt-get update
sudo apt-get install python3.9 
sudo apt-get install node
sudo apt-get install docker

echo "${yellow}Create virtual env"${clear}
python3.9 -m pip install virtualenv
virtualenv --python=$(which python3.9) venv
. $PWD/venv/bin/activate

echo "${yellow}Install requirements${clear}"
pip install -r requirements.txt


