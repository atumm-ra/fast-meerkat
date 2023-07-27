

from beanie import Document

from pymongo import IndexModel

from atumm.user.core.models import UserModel
from atumm.user.dataproviders.beanie.common.mixins import TimestampMixin


class User(Document, UserModel, TimestampMixin):
    class Beanie:
        document_model_name = "users"

    class Settings:
        indexes = [
            IndexModel("email", unique=True),
            IndexModel("username", unique=True),
        ]
        is_root = True

    

    
