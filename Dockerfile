FROM python:3.12.2

RUN apt-get update -y && apt-get -y install sudo git nano curl ffmpeg &&\
    apt-get clean && apt-get autoclean && apt-get autoremove --yes && rm -rf /var/lib/apt/lists/*

WORKDIR /home

RUN adduser --system --group dockerdc

RUN git clone https://github.com/Ex3cut4ble/DiscordGachiBot ./dockerdc/
RUN chown -R dockerdc:dockerdc ./dockerdc/* &&\
    chmod -R 0755 ./dockerdc/*

RUN pip install --no-cache-dir -r ./dockerdc/requirements.txt

USER dockerdc

ENTRYPOINT [ "./dockerdc/docker_entrypoint.sh" ]