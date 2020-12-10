#!/bin/bash

#Clear project source code

sudo rm -rf /var/www/kinujo_production
sudo rm -rf /home/ec2-user/git/kinujo_production
sudo mkdir /home/ec2-user/git/kinujo_production

cd /home/ec2-user/git/kinujo_production
eval `ssh-agent`
sudo chmod 400 /home/ec2-user/.ssh/id_rsa
ssh-add /home/ec2-user/.ssh/id_rsa

remote_repo=git@bitbucket.org:c2sg/kinujo.git
local_repo=/home/ec2-user/git/kinujo_production

if [ -d $local_repo/.git ]; then pushd $local_repo; git pull; popd; else git clone $remote_repo . -b master --depth 1; fi

#Copy source code to project folder
sudo rsync -avz --exclude '.git' /home/ec2-user/git/kinujo_production/ /var/www/kinujo_production
sudo mkdir /var/www/kinujo_production/logs
