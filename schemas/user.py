from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Schema for creating a new user
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

# Schema for updating an existing user
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None  # Password is optional for updates

# Schema for returning user details in API responses
class UserResponse(BaseModel):
    user_id: int
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Allows Pydantic to work with SQLAlchemy models directly

# Schema for logging in a user (email and password required)
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for token data (JWT token + user ID)
class TokenData(BaseModel):
    access_token: str
    token_type: str
    user_id: int  # Add user_id field
    first_name : str


class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    email: EmailStr
    otp: str
    new_password: str
