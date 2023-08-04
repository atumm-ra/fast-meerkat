import os

from buti import ButiStore
from fastapi import FastAPI

from thisapp.buti.bootloader import bootloader
from thisapp.buti.keys import ContainerKeys

store: ButiStore = bootloader.boot()
app: FastAPI = store.get(ContainerKeys.app)