FROM python:3.11.5-bullseye

ENV DOCKERIZE_VERSION v0.7.0

RUN apt-get update \
    && apt-get install -y wget \
    && wget -O - https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz | tar xzf - -C /usr/local/bin \
    && apt-get autoremove -yqq --purge wget && rm -rf /var/lib/apt/lists/*

ENV PYTHONBUFFERED=true
ENV STAGE=dev

WORKDIR /home

COPY ./ /home/
COPY ./.env /home/
RUN pip install --upgrade pip
RUN pip install pdm


RUN chmod +x /home/.docker/api/dev/startup.sh
ENTRYPOINT /home/.docker/api/dev/startup.sh