# app/models/predict.py
from sqlalchemy import Column, Integer, String, Float
from database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    predicted_class = Column(String)
    confidence = Column(Float)
    image_url = Column(String)
