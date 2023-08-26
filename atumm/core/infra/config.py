from pydantic import BaseSettings


class Config(BaseSettings):
    STAGE: str = "dev"
    DEBUG: bool
    