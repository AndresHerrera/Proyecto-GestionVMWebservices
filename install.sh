#!/bin/bash
sudo apt-get update -y
sudo apt-get install -y python-pip python-dev build-essential
sudo pip install --upgrade pip
sudo pip install -r requirements.txt
sudo apt-get install -y virtualbox
