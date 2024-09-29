# app/schemas/review.py
from pydantic import BaseModel, Field

class ReviewSchema(BaseModel):
    review: str
    rate: float = Field(..., ge=0, le=5)  # Ensures rating is between 0 and 5

    class Config:
        orm_mode = True
