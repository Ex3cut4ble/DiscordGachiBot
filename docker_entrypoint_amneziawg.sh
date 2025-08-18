#!/bin/sh
awg-quick up wg0
sudo sh -c "su gachibot"

cd /home/gachibot
python3.12 main.py

sudo sh -c "su root"
awg-quick down wg0
