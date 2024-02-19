#!/bin/bash

# Create a local user csye6225 with primary group csye6225
sudo groupadd csye6225
sudo useradd -r -g csye6225 -s /usr/sbin/nologin csye6225
# sudo chown -R csye6225:csye6225 /tmp/

# Check Python version
python3 -V

# # Install unzip if not already installed
# sudo yum install -y unzip

# # Copy the webapp-main.zip file to the /tmp directory
# sudo cp /path/to/packer/webapp-main.zip /tmp/

# # Unzip the webapp-main.zip file into /opt/myapp
# sudo unzip /tmp/webapp-main.zip -d /opt/myapp

# # Ensure that the contents of the zip file are owned by user csye6225 and group csye6225
# sudo chown -R csye6225:csye6225 /opt/myapp

# Print success message
echo "User setup and file extraction completed successfully."
echo "============================================================================================================================================================================="