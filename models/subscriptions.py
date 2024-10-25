from sqlalchemy import Column, Integer, String, Boolean, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    subscription_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    subscription_type = Column(String, nullable=False)  # 'Tech', 'Analyst', 'Scientist'
    billing_frequency = Column(String, nullable=False)  # 'monthly', 'annually'
    subscription_plan = Column(String, nullable=False)  # 'premium', 'basic'
    subscription_price = Column(Numeric(10, 2), nullable=False)
    subscription_status = Column(String, nullable=False, default="active")
    ids_per_month = Column(Integer, default=0)  # IDs per month (0 for unlimited)
    savings_percentage = Column(Numeric(5, 2), default=0.0)
    subscription_start_date = Column(DateTime, default=datetime.utcnow)
    subscription_end_date = Column(DateTime)
    free_id_count = Column(Integer, default=0)
    purchased_id_count = Column(Integer, default=0)
    last_reset_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

