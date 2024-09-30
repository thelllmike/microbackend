# app/models/predict.py
from sqlalchemy import Column, Integer, String, Float, Text
from database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    predicted_class = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    image_url = Column(String, nullable=False)

    # New columns
    about = Column(Text, nullable=True)  # Storing long descriptions
    articles = Column(Text, nullable=True)  # Storing articles as JSON string
    key_research_topics = Column(Text, nullable=True)  # Storing research topics as JSON string
    uses = Column(Text, nullable=True)  # Storing long text
    illnesses_caused = Column(Text, nullable=True)  # Storing long text