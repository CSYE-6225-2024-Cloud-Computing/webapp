#!/bin/bash

# Enable PostgreSQL module
sudo dnf module enable postgresql:15 -y

# Install PostgreSQL server
sudo dnf install -y postgresql-server

# Initialize PostgreSQL database
sudo postgresql-setup --initdb

# Start PostgreSQL service
sudo systemctl start postgresql

# Enable PostgreSQL to start on boot
sudo systemctl enable postgresql

# Set password for the postgres user in PostgreSQL
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"

# Update pg_hba.conf file to use md5 authentication
sudo sed -i 's/^\(host.*all.*all.\)\(ident\)\(.*\)$/\1md5\3/g' /var/lib/pgsql/data/pg_hba.conf

# Restart PostgreSQL to apply changes
sudo systemctl restart postgresql

# Create a database named 'test01'
sudo -u postgres psql -c "CREATE DATABASE test01;"

# Install unzip utility
sudo dnf makecache
sudo dnf install -y unzip

# Print completion message
echo "Database Initialization completed."
echo "============================================================================================================================================================================="
