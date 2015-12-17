#!/bin/bash
# Setup an EC2 development environment (with virtual env).

virtual_envs=largescale
install_dir=/home/ubuntu/${virtual_envs}

## Install Ruby and Brew
sudo apt-get install ruby
## brew for linux:
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/linuxbrew/go/install)"
## brew for mac:
# ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
export PATH="$HOME/.linuxbrew/bin:$PATH"
export MANPATH="$HOME/.linuxbrew/share/man:$MANPATH"
export INFOPATH="$HOME/.linuxbrew/share/info:$INFOPATH"
## Add below if not in .bashrc already
# echo '
# export PATH="$HOME/.linuxbrew/bin:$PATH"
# export MANPATH="$HOME/.linuxbrew/share/man:$MANPATH"
# export INFOPATH="$HOME/.linuxbrew/share/info:$INFOPATH"
# ' >> ~/.bashrc

sudo apt-get update -y
sudo apt-get install git -y
sudo apt-get install libmysqlclient-dev -y

export DEBIAN_FRONTEND=noninteractive
sudo apt-get -q -y install mysql-server -y

sudo apt-get install python-dev python-pip -y
sudo pip install virtualenv

sudo mkdir -p $install_dir
sudo chown ubuntu:ubuntu $install_dir

# The rest of these steps can be executed manually on the machine.
cd $install_dir
sudo virtualenv --system-site-packages .
source ./bin/activate
sudo pip install Django==1.8
sudo pip install django-debug-toolbar==1.3.2
sudo pip install MySQL-python==1.2.5
# echo "To deactivate run:"
# echo "\$ deactivate"

# Install grpcio
sudo apt-get install protobuf-compiler
echo "deb http://http.debian.net/debian jessie-backports main" | sudo tee -a /etc/apt/sources.list
sudo apt-get update
sudo apt-get install libgrpc-dev
sudo pip install --pre grpcio
curl -fsSL https://goo.gl/getgrpc | bash -s python
sudo pip install protobuf

# Install Redis
sudo pip install redis
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
# Test Redis
sudo apt-get install tcl8.5
make test
sudo apt-get install redis-server
cd ../

# Get the source files
git clone https://github.com/quiquelores/Scalica-Search.git scalica

# Install NLTK
sudo pip install -U nltk

# set up the database
cd ${install_dir}/scalica/scalica/db
./install_db.sh
cd ${install_dir}/scalica/scalica/web/scalica
python manage.py makemigrations
python manage.py migrate

sudo chown -R ubuntu:ubuntu $install_dir
sudo chown ubuntu:ubuntu /tmp/db.debug.log


# TO RUN, you must run the dev server, the indexing server, and the redis server:

## 1) Run dev server:
# python ${install_dir}/scalica/scalica/web/scalica/manage.py runserver 0.0.0.0:8000

## 2) Run indexing server:
# python ${install_dir}/scalica/search-service/search_server.py
## Note: You might get an error that says: __init__() got an unexpected keyword argument 'syntax'
## A work around is to go into ${install_dir}/scalica/search-service/search_pb2.py and delete all lines that say 'syntax='proto2'

## 3) Run Redis server:
# redis-server

# Also, remember to make ec2 instance have security group with Custom TCP Rule at port 8000
