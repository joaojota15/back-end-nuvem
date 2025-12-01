from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    steam_id: Optional[str] = None

    model_config = {"from_attributes": True}

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: str

class LoginIn(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = {"from_attributes": True}

class UserProfile(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    steam_id: Optional[str] = None

    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    name: str
