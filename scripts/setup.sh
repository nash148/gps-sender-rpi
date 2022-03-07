#!/bin/bash

echo "Starting setup..."

# pip install
echo "pip install..."
sudo pip3 install -r ../requirenments.txt

echo "Create /home/pi/gps-sender/scripts dir"
mkdir -p /home/pi/gps-sender/scripts

echo "Copie the relevant scripts"
cp ./run_gps_sender.sh /home/pi/gps-sender/scripts

echo "Change the scripts permissions"
sudo chmod +x /home/pi/gps-sender/scripts/run_gps_sender.sh

echo "Copy the services to systemd dir"
sudo cp ./services/gps-sender.service /etc/systemd/system/

sudo systemctl enable gps-sender.service
echo "Enable gps-sender service"

echo "Done!!"
