import bcrypt
from enum import StrEnum, auto
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr, Field, validator

from atumm.app.infra.config import get_config

class StatusEnum(StrEnum):
    ACTIVE = auto()
    LOCKED = auto()
    DELETED = auto()

class UserModel(BaseModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: EmailStr = Field(str)
    password: str = Field(..., min_length=8, description="The user's hashed password")
    username: str = Field(
        str, min_length=3, max_length=255, description="The user's unique username"
    )
    is_admin: bool = Field(
        False, description="Indicates if the user has admin privileges"
    )
    salt: str = Field(default_factory=bcrypt.gensalt,description="password salt")
    status: StatusEnum = Field(StatusEnum.ACTIVE)
    # Optional fields
    
    first_name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="The user's first name"
    )
    last_name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="The user's last name"
    )
    device_id: Optional[str] = Field(None)
    

    class Config:
        bson_encoders: dict = {UUID: str}
        arbitrary_types_allowed: bool = True

    @validator("password")
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value

    def _get_pass_key(self):
        config = get_config()
        pass_key = config.PASSWORD_KEY
        return pass_key

    def encrypt_password(self):
        pass_key = self._get_pass_key()
        pass_combination = self.password + pass_key + self.salt
        self.password = bcrypt.hashpw(pass_combination, self.salt)

    def is_password_valid(self, password: str) -> bool:
        input_pass_hashed = bcrypt.hashpw(
            password + self._get_pass_key() + self.salt, self.salt
        )
        return self.password == input_pass_hashed

    def lock(self):
        self.status = StatusEnum.LOCKED

    def is_locked(self) -> bool:
        return self.status == StatusEnum.LOCKED