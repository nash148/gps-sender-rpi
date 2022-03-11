#!/bin/bash

sleep 5

cd /home/pi/clones/gps-sender-rpi
sudo python ./src/main.py > /dev/tty1
