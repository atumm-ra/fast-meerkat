from uuid import UUID

from pydantic import BaseModel, Field


class GetUserListResponseSchema(BaseModel):
    class Config:
        orm_mode = True

    id: UUID = Field(..., description="ID")
    email: str = Field(..., description="Email")
    username: str = Field(..., description="username")


class CreateUserResponseSchema(BaseModel):
    class Config:
        orm_mode = True

    email: str = Field(..., description="Email")
    username: str = Field(..., description="username")


class LoginResponseSchema(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")
