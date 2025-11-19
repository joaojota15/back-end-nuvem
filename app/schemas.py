from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str            
    username: str      
    email: EmailStr

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

class UserProfile(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    steam_id: Optional[str] = None
    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    title: str
    description: str
    category: str

class PostOut(BaseModel):
    id: str
    title: str
    description: str
    category: str
    author_id: str
    created_at: str
    class Config:
        from_attributes = True
