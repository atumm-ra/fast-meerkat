from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str = Field(..., description="Email")
    password: str = Field(..., description="Password")
    device_id: str = Field(..., description="Device ID")


class RefreshTokenRequest(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")


class VerifyTokenRequest(BaseModel):
    token: str = Field(..., description="Token")
