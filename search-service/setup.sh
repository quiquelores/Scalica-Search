#!/bin/bash

virtual_envs=largescale
install_dir=/home/ubuntu/${virtual_envs}

apt-get update -y
apt-get install git -y

apt-get install python-dev python-pip -y
pip install virtualenv
pip install setuptools twine

mkdir -p $install_dir
chown ubuntu:ubuntu $install_dir

virtualenv --system-site-packages .
source ./bin/activate

wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make

echo "deb http://http.debian.net/debian jessie-backports main" | \
sudo tee -a /etc/apt/sources.list

sudo apt-get update -y
sudo apt-get install libgrpc-dev -y
sudo pip install --pre grpcio

cd $install_dir
git clone https://github.com/quiquelores/Scalica-Search.git

cd Scalica-Search/search-service/

protoc -I . --python_out=. --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_python_plugin` search.proto

python search_server.py
