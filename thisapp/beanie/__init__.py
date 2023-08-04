from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from thisapp.config import get_config
from atumm.services.user.dataproviders.beanie.models import User


async def init_my_beanie(client: AsyncIOMotorClient, db_name: str):
    db = client[db_name]

    await init_beanie(db, document_models=[User])
    return db
