#!/bin/bash

# Build up the tsalon user so that it can run the site.  This user cannot sudo.

chmod 600 .pgpass

git clone https://github.com/TSalon/PhotoUpload.git

# sort out virtualenv settings
export VIRTUALENVWRAPPER_PYTHON=`which python3`

echo '' >> ~/.profile
echo 'export WORKON_HOME=$HOME/.venv' >> ~/.profile
echo 'export PROJECT_HOME=$HOME' >> ~/.profile
echo 'export VIRTUALENVWRAPPER_PYTHON=`which python3`' >> ~/.profile
echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.profile

source ~/.profile

# create virtualenv
mkvirtualenv tsalon --python=`which python3`
cd ~/PhotoUpload/web/site
pip3 install -r requirements.txt