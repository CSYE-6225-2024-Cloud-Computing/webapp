#!/bin/bash

# Add the Ops Agent repository
curl -sSO https://dl.google.com/cloudagents/add-monitoring-agent-repo.sh
sudo bash add-monitoring-agent-repo.sh --also-install

# Install the Ops Agent
sudo apt-get update && sudo apt-get install -y stackdriver-agent

# Start the Ops Agent service
sudo service stackdriver-agent start
