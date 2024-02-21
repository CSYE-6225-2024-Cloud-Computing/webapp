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

# Back up pg_hba.conf
sudo cp /var/lib/pgsql/data/pg_hba.conf /var/lib/pgsql/data/pg_hba.conf.bak

# Allow password authentication for localhost connections
sudo chmod u+w /var/lib/pgsql/data/pg_hba.conf
sudo sed -i '/127.0.0.1\/32/s/ident/md5/' /var/lib/pgsql/data/pg_hba.conf
sudo sed -i '/::1\/128/s/ident/md5/' /var/lib/pgsql/data/pg_hba.conf
grep 'md5' /var/lib/pgsql/data/pg_hba.conf
sudo cat /var/lib/pgsql/data/pg_hba.conf

# Restart PostgreSQL to apply changes
sudo systemctl restart postgresql

# Create a database named 'test01'
sudo -u postgres psql -c "CREATE DATABASE test01;"

# Install unzip utility
sudo dnf makecache
sudo dnf install -y unzip

# Print completion message
echo '================================================================================================================================================'
echo 'Database Initialization completed.'
echo '================================================================================================================================================'
