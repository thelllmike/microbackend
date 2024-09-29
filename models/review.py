# app/models/review.py
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    review = Column(Text, nullable=False)
    rate = Column(Float, nullable=False)

    user = relationship("User", back_populates="reviews")
