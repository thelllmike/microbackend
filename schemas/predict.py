# schemas/predict.py
from pydantic import BaseModel
from typing import List, Optional

# Define the structure for articles
class Article(BaseModel):
    name: str
    url: str

# Define the structure for the prediction request
class PredictionRequest(BaseModel):
    user_id: int
    predicted_class: str
    confidence: float
    image_url: str
    about: Optional[str] = None
    articles: Optional[List[Article]] = []
    key_research_topics: Optional[List[str]] = []
    uses: Optional[str] = None
    illnesses_caused: Optional[str] = None



class PredictionResponse(BaseModel):
    predicted_class: str
    confidence: float
    image_url: str
    about: Optional[str] = None
    articles: Optional[List[Article]] = []
    key_research_topics: Optional[List[str]] = []
    uses: Optional[str] = None
    illnesses_caused: Optional[str] = None