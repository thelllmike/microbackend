from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SubscriptionCreate(BaseModel):
    user_id: int  # Add user_id field
    subscription_type: str
    billing_frequency: str
    subscription_plan: str
    subscription_price: float
    ids_per_month: Optional[int] = 0
    savings_percentage: Optional[float] = 0.0
    subscription_end_date: Optional[datetime]
    free_id_count: Optional[int] = 0
    purchased_id_count: Optional[int] = 0

class SubscriptionUpdate(BaseModel):
    subscription_status: Optional[str]
    subscription_end_date: Optional[datetime]
    free_id_count: Optional[int]
    purchased_id_count: Optional[int]

class SubscriptionResponse(BaseModel):
    subscription_id: int
    subscription_type: str
    billing_frequency: str
    subscription_plan: str
    subscription_price: float
    subscription_status: str
    ids_per_month: Optional[int]
    savings_percentage: Optional[float]
    subscription_start_date: datetime
    subscription_end_date: Optional[datetime]
    free_id_count: int
    purchased_id_count: int

    class Config:
        orm_mode = True