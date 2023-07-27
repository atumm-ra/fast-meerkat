#!/bin/bash

# install deps
    pdm config python.use_venv false
pdm sync
pdm sync --group dev

dockerize -wait tcp://mongo:27017 -timeout 20s

pdm run uvicorn atumm.app.infra.app.server:app --host 0.0.0.0 --port 8000 --reload
