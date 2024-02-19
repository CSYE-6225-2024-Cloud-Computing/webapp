#!/bin/bash

# Update the system and install required packages
sudo yum update -y
sudo yum install -y epel-release
sudo yum install -y python39  # Add unzip to the list of installed packages

# Verify Python 3.9 installation
python3.9 --version

# Verify Python 3.9 installation
which python3.9 

# Print completion messages
echo '================================================================================================================================================'
echo 'Python Installations completed.'
echo '================================================================================================================================================'
