from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from atumm.app.infra.config import get_config
from atumm.user.dataproviders.beanie.models import User


async def init_my_beanie():
    config = get_config()
    db = AsyncIOMotorClient(config.MONGO_URL, uuidRepresentation="standard").account

    await init_beanie(db, document_models=[User])
    return db
