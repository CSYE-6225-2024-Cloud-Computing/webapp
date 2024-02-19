# Create a local group csye6225
sudo groupadd csye6225

# Create a local user csye6225 with the specified requirements
sudo useradd -m -g csye6225 -s /usr/sbin/nologin csye6225
echo '================================================================================================================================================'
echo 'User Initialization completed.'
echo '================================================================================================================================================'
