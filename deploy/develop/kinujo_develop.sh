sudo rm -rf /var/www/kinujo_develop
sudo rm -rf /home/ec2-user/git/kinujo
sudo mkdir /home/ec2-user/git/kinujo

cd /home/ec2-user/git/kinujo
eval `ssh-agent`
sudo chmod 400 /home/ec2-user/.ssh/id_rsa
ssh-add /home/ec2-user/.ssh/id_rsa

remote_repo=git@bitbucket.org:c2sg/kinujo.git
local_repo=/home/ec2-user/git/kinujo

if [ -d $local_repo/.git ]; then pushd $local_repo; git pull; popd; else git clone $remote_repo . -b demo --depth 1; fi

#Copy source code to project folder
sudo rsync -avz --exclude '.git' /home/ec2-user/git/kanehira/ /var/www/kinujo_develop

#Run migrate
/var/www/.env/bin/pip install -r /var/www/kinujo_develop/requirements.txt
/var/www/.env/bin/python /var/www/kinujo_develop/manage_demo.py migrate

#permission for logs
sudo chmod -R 0777 /var/log/httpd/kinujo_develop/
sudo chmod -R 0777 /var/www/kinujo_develop/logs/
