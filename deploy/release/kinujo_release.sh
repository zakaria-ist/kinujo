#!/bin/bash

#Clear project source code

sudo rm -rf /var/www/kinujo_release
sudo rm -rf /home/ec2-user/git/kinujo_release
sudo mkdir /home/ec2-user/git/kinujo_release

cd /home/ec2-user/git/kinujo_release
eval `ssh-agent`
sudo chmod 400 /home/ec2-user/.ssh/id_rsa
ssh-add /home/ec2-user/.ssh/id_rsa

remote_repo=git@bitbucket.org:c2sg/kinujo.git
local_repo=/home/ec2-user/git/kinujo_release

if [ -d $local_repo/.git ]; then pushd $local_repo; git pull; popd; else git clone $remote_repo . -b release --depth 1; fi

#Copy source code to project folder
sudo rsync -avz --exclude '.git' /home/ec2-user/git/kinujo_release/ /var/www/kinujo_release
sudo mkdir /var/www/kinujo_release/logs

#Run migrate
/var/www/.env/bin/pip install -r /var/www/kinujo_release/requirements.txt
/var/www/.env/bin/python /var/www/kinujo_release/kinujo/settings_release.py migrate

#permission for logs
sudo chmod -R 0777 /var/log/httpd/kinujo_release/
sudo chmod -R 0777 /var/www/kinujo_release/logs/
