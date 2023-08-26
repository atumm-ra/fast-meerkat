from uuid import UUID

from pydantic import BaseModel, Field


class GetUsersResponse(BaseModel):
    id: UUID = Field(..., description="ID")
    email: str = Field(..., description="Email")
    username: str = Field(..., description="username")


class RegisterResponse(BaseModel):
    email: str = Field(..., description="Email")
    username: str = Field(..., description="username")


class LoginResponse(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")
