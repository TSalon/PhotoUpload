#!/bin/bash

# Build the initial machine setup using the admin user.
# This user can sudo, others cannot.

# Bring machine up to date
sudo apt-get update
sudo apt-get upgrade -y

# install and configure email sender postfix
sudo debconf-set-selections <<< "postfix postfix/mailname string tsalon.co.uk"
sudo debconf-set-selections <<< "postfix postfix/main_mailer_type string 'Internet Site'"
sudo apt-get install -y postfix

# install required software as root
sudo apt-get install git python3-pip nginx postgresql-client -y
export VIRTUALENVWRAPPER_PYTHON=`which python3`
sudo pip3 install -U pip
sudo pip3 install -U virtualenv virtualenvwrapper

# sort out virtualenv settings
echo '' >> ~/.profile
echo 'export WORKON_HOME=$HOME/.venv' >> ~/.profile
echo 'export PROJECT_HOME=$HOME' >> ~/.profile
echo 'export VIRTUALENVWRAPPER_PYTHON=`which python3`' >> ~/.profile
echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.profile

# Create tsalon user and group, and copy in certificate and .pgpass
sudo addgroup ${username}
sudo adduser ${username} --ingroup ${username} --disabled-password --gecos ""
#sudo bash -c echo ${username}:${password} | chpasswd
sudo mkdir /home/${username}/.ssh
sudo cp ~/.ssh/authorized_keys /home/${username}/.ssh
sudo chown -R ${username}:${username} /home/${username}/.ssh

# Make sure copied in files on tsalon user are owned by tsalon:tsalon
cd /home/${username}
sudo chown -R ${username}:${username} /home/${username}

# create log file folders
sudo mkdir /var/log/tsalon
sudo chmod a+rwx /var/log/tsalon

# run bbr gunicorn server
sudo cp ~/init-gu-tsalon /etc/init.d/gu-tsalon
sudo chmod a+x /etc/init.d/gu-tsalon
sudo chown root:root /etc/init.d/gu-tsalon
sudo systemctl enable gu-tsalon

# configure nginx
sudo mkdir -p /var/log/tsalon
sudo cp ~/nginx-tsalon /etc/nginx/sites-available/tsalon
sudo ln -s /etc/nginx/sites-available/tsalon /etc/nginx/sites-enabled/tsalon
sudo service stop nginx
sudo service start nginx
date
