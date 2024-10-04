#!/bin/sh

curl -sL https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz | tar -Jxf - -C ./
mv ./ffmpeg-master-latest-linux64-gpl/bin/ffmpeg ./
rm -rf ./ffmpeg-master-latest-linux64-gpl
chmod 0755 ./ffmpeg