from pydantic import BaseModel, EmailStr
from typing import Optional

# Base schema that can be inherited by other schemas
class ReviewBase(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    review: str
    rate: float

# Schema for creating a new review
class ReviewCreate(ReviewBase):
    user_id: int

# Schema for updating an existing review
class ReviewUpdate(ReviewBase):
    pass  # Optional: Fields can be added for partial updates if necessary

# Schema for reading review data (response from API)
class Review(ReviewBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True  # Enable ORM mode to allow using SQLAlchemy models directly