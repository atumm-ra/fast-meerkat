import os

from buti import ButiStore
from fastapi import FastAPI

from atumm.app.infra.buti.bootloader import bootloader
from atumm.app.infra.buti.keys import ContainerKeys

store: ButiStore = bootloader.boot()
app: FastAPI = store.get(ContainerKeys.app)
