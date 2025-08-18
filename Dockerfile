FROM python:3.12.2

RUN apt-get update -y && apt-get -y install sudo git nano curl dos2unix ffmpeg &&\
    apt-get clean && apt-get autoclean && apt-get autoremove --yes && rm -rf /var/lib/apt/lists/*

WORKDIR /home

RUN adduser --system --group gachibot

RUN git clone https://github.com/Ex3cut4ble/DiscordGachiBot ./gachibot/
RUN chown -R gachibot:gachibot ./gachibot/* &&\
    chmod -R 0755 ./gachibot/*

RUN pip install --no-cache-dir -r ./gachibot/requirements.txt

RUN dos2unix ./gachibot/docker_entrypoint.sh

USER gachibot

ENTRYPOINT [ "./gachibot/docker_entrypoint.sh" ]
