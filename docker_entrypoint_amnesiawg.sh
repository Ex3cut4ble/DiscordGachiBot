#!/bin/sh
awg-quick up wg0
sudo sh -c "su dockerdc"

cd /home/dockerdc
python3.12 main.py

sudo sh -c "su root"
awg-quick down wg0
