from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "user"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshRequest(BaseModel):
    refresh_token: str


class EditProfile(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
class ChangePassword(BaseModel):
    current_password: str
    new_password: str
