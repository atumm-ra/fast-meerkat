FROM golang:1.20.3-alpine3.17 AS builder

WORKDIR /tmp/

RUN wget https://github.com/jwilder/dockerize/archive/refs/heads/master.zip \
    && unzip master.zip && ls -la  && cd dockerize-master \
    && GOOS=linux GOARCH=amd64 go build -ldflags "$(LDFLAGS)" -o /usr/local/bin/dockerize \
    && cd /home && rm -rf /tmp/dockerize-master


FROM python:3.11.5-bullseye


ENV PYTHONBUFFERED=true

WORKDIR /home
COPY --from=builder /usr/local/bin/dockerize /usr/local/bin/dockerize

COPY ./ /home

ENV STAGE=dev
# deps
RUN pip install --upgrade pip
RUN pip install pdm


RUN chmod +x /home/.docker/api/startup.sh
ENTRYPOINT /home/.docker/api/startup.sh