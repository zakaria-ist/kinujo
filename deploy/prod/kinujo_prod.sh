#Clear project source code

sudo rm -rf /var/www/kinujo

cd /home/ec2-user/git/kinujo
eval `ssh-agent`
sudo chmod 400 /home/ec2-user/.ssh/id_rsa
ssh-add /home/ec2-user/.ssh/id_rsa

remote_repo=git@bitbucket.org:c2sg/kinujo.git
local_repo=/home/ec2-user/git/kinujo

if [ -d $local_repo/.git ]; then pushd $local_repo; git pull; popd; else git clone $remote_repo . -b master --depth 1; fi

#Copy source code to project folder
sudo rsync -avz --exclude '.git' /home/ec2-user/git/kinujo/ /var/www/kinujo

#Run migrate
/var/www/.env/bin/pip install -r /var/www/kanehira/requirements.txt
/var/www/.env/bin/python /var/www/kinujo/kinujo/settings_production.py migrate

#permission for logs
sudo chmod -R 0777 /var/log/httpd/kinujo/
sudo chmod -R 0777 /var/www/kinujo/logs/
