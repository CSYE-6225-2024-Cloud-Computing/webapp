#!/bin/bash

# Update system packages
sudo dnf update -y

# Install development tools and dependencies
sudo dnf groupinstall -y 'development tools'
sudo dnf install -y wget openssl-devel bzip2-devel libffi-devel

# Download and install Python 3.9.1
sudo curl -O https://www.python.org/ftp/python/3.9.1/Python-3.9.1.tgz
sudo tar -xvf Python-3.9.1.tgz
cd Python-3.9.1
sudo ./configure --enable-optimizations
sudo make
sudo make install


# Check Python version
python3 -V

#which python
which python3

# Print success message
echo "Python installation completed successfully."

