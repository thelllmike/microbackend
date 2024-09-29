from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True, nullable=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    # Fields for OTP
    otp = Column(String, nullable=True)
    otp_created_at = Column(DateTime, default=datetime.utcnow)
    
    # Other fields
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    reviews = relationship("Review", back_populates="user")
    tickets = relationship("Ticket", back_populates="user")
    features = relationship("Feature", back_populates="user")
    equipments = relationship("Equipment", back_populates="user")