from pydantic import BaseModel, Field


class AuthenticatedTokensResponse(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")