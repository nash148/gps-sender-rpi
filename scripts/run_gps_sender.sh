#!/bin/bash

while ! ping -c 1 -W 1 8.8.8.8; do
    echo "Waiting for network - network interface might be down..." > /dev/tty1
    sleep 1
done

cd /home/pi/clones/gps-sender-rpi
sudo python ./src/main.py > /dev/tty1
