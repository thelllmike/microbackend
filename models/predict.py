from sqlalchemy import Column, Integer, String, Float, Text, JSON, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    predicted_class = Column(String(255), nullable=False)
    confidence = Column(Float, nullable=False)
    image_url = Column(Text, nullable=False)
    about = Column(Text)
    key_research_topics = Column(JSON)
    uses = Column(Text)
    illnesses_caused = Column(Text)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'), nullable=False)

    # Relationship with the Article model
    articles = relationship("Article", back_populates="prediction")


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer, ForeignKey("predictions.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    url = Column(Text, nullable=False)

    # Relationship with the Prediction model
    prediction = relationship("Prediction", back_populates="articles")