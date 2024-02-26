#!/bin/bash

# Install unzip utility 
sudo dnf install -y unzip

# Create the target directory if it doesn't exist
sudo mkdir -p /home/csye6225/webapp

# Install application dependencies and copy artifacts and configuration files
sudo unzip /tmp/webapp.zip -d /home/csye6225/webapp

echo '================================================================================================================================================'
echo 'Unzipping Completed.'
echo '================================================================================================================================================'


# User Creation Installation
sudo chmod +x /home/csye6225/webapp/packer-webapp/userInstall.sh
sudo /home/csye6225/webapp/packer-webapp/userInstall.sh

# Copy service file to the correct location
sudo cp /home/csye6225/webapp/service/webapp.service /etc/systemd/system/webapp.service
sudo chown csye6225:csye6225 /etc/systemd/system/webapp.service
sudo chmod 550 /etc/systemd/system/webapp.service

# Database Installation
# sudo chmod +x /home/csye6225/webapp/packer-webapp/databaseInstall.sh
# sudo /home/csye6225/webapp/packer-webapp/databaseInstall.sh

# Python Installation
sudo chmod +x /home/csye6225/webapp/packer-webapp/pythonInstall.sh
sudo /home/csye6225/webapp/packer-webapp/pythonInstall.sh

# Pip Requirements Installation
sudo pip3.9 install -r /home/csye6225/webapp/app/requirements.txt 

echo '================================================================================================================================================'
echo 'Requirements.txt installations completed.'
echo '================================================================================================================================================'

# Give ownership permission to csye6225
sudo chown -R csye6225:csye6225 /home/csye6225/webapp/
# TODO: add 755 permission to the app dir with R flag

echo '================================================================================================================================================'
echo 'Ownership of the application directory set to the dedicated user - csye6225'
echo '================================================================================================================================================'

# Reload systemd to pick up changes
sudo systemctl daemon-reload

# Enable the webapp.service to start on boot
sudo systemctl enable webapp.service

# Start the webapp.service
sudo systemctl start webapp.service

echo '================================================================================================================================================'
echo 'Ownership of the application directory set to the dedicated user - csye6225'
echo '================================================================================================================================================'
echo '================================================================================================================================================'
echo 'Custom image setup completed'
echo '================================================================================================================================================'
