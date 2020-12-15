#!/bin/bash

#Run migrate
/var/www/.env/bin/pip install -r /var/www/kinujo_production/requirements.txt
/var/www/.env/bin/python /var/www/kinujo_production/manage.py migrate --settings kinujo.settings_production

#permission for logs
sudo chmod -R 0777 /var/log/httpd/kinujo_production/
sudo chmod -R 0777 /var/www/kinujo_production/logs/

sudo service httpd restart
