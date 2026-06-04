from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    user_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    email: EmailStr


class User(BaseModel):
    user_id: str
    name: str
    email: EmailStr
    created_at: datetime
    status: str = "CREATED"