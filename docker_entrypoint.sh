#!/bin/sh

cd /home/dockerdc/

if ! [ -e ./ffmpeg ]
then
    echo "FFMPEG not found, installing..."
    ./install_ffmpeg.sh
fi

python3 main.py
sleep 2147483647