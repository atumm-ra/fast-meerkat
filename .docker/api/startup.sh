#!/bin/bash

# install deps
pdm sync



dockerize -wait tcp://mongo:27017 -timeout 20s

pdm run gunicorn --bind 0.0.0.0:8000 -w 4 -k uvicorn.workers.UvicornWorker --timeout 120 atumm.app.infra.app.server:app
