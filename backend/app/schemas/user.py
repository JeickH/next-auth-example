from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class UserPlan(str, Enum):
    FREE = "free"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    document: str
    document_type: str
    plan: UserPlan = UserPlan.FREE

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    plan: Optional[UserPlan] = None

class UserInDBBase(UserBase):
    id: int
    is_active: bool
    is_superuser: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
    is_superuser: bool = False

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
