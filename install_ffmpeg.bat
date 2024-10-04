curl -sL https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip -o .\ffmpeg-master-latest-win64-gpl.zip
tar -xf .\ffmpeg-master-latest-win64-gpl.zip -C .\
move .\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe .\ >nul
rd /s /q .\ffmpeg-master-latest-win64-gpl
del .\ffmpeg-master-latest-win64-gpl.zip