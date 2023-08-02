import os
from functools import lru_cache

from pydantic import BaseSettings


class Config(BaseSettings):
    STAGE: str = "dev"
    DEBUG: bool

    APP_HOST: str
    APP_PORT: int

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    PASSWORD_KEY: str

    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_USER: str
    MONGO_PASS: str
    MONGO_DB: str
    MONGO_URL: str
    MONGO_COLLECTION: str


class DevelopmentConfig(Config):
    pass


class LocalConfig(Config):
    pass


class ProductionConfig(Config):
    pass


class TestConfig(Config):
    pass


@lru_cache
def get_config() -> Config:
    env = os.getenv("STAGE", "local")
    config_type = {
        "local": LocalConfig(_env_file=".env"),
        "test": TestConfig(_env_file=".env.test"),
        "dev": DevelopmentConfig(_env_file=".env"),
        "prod": ProductionConfig(_env_file=".env"),
    }
    return config_type[env]
