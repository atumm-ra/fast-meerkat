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


class DevelopmentConfig(Config):
    pass


class LocalConfig(Config):
    pass


class ProductionConfig(Config):
    pass


class TestConfig(Config):
    pass



def get_config() -> Config:
    env = os.environ['STAGE']
    
    match env:
        case 'local':
            return LocalConfig(_env_file=".env")
        case 'test':
            return TestConfig(_env_file=".env.test")
        case 'dev':
            return DevelopmentConfig(_env_file=".env")
        case 'prod':
            return ProductionConfig(_env_file=".env")
        case _:
            raise ValueError("invalid '{env}' stage")
