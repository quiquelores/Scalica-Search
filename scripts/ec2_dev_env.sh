#!/bin/bash
# Setup an EC2 development environment (with virtual env).

virtual_envs=largescale
install_dir=/home/ubuntu/${virtual_envs}

apt-get update -y
apt-get install git -y
apt-get install libmysqlclient-dev -y

export DEBIAN_FRONTEND=noninteractive
apt-get -q -y install mysql-server -y

apt-get install python-dev python-pip -y
pip install virtualenv

mkdir -p $install_dir
chown ubuntu:ubuntu $install_dir

# The rest of these steps can be executed manually on the machine.
cd $install_dir
virtualenv --system-site-packages .
source ./bin/activate
pip install Django==1.8
pip install django-debug-toolbar==1.3.2
pip install MySQL-python==1.2.5
# echo "To deactivate run:"
# echo "\$ deactivate"

# Get the source files
git clone http://23.236.49.28/git/scalica.git scalica

# set up the database
cd ${install_dir}/scalica/db
./install_db.sh
cd ${install_dir}/scalica/web/scalica
python manage.py makemigrations
python manage.py migrate

chown -R ubuntu:ubuntu $install_dir
chown ubuntu:ubuntu /tmp/db.debug.log
## Start the dev server
# python manage.py runserver 0.0.0.0:8000
