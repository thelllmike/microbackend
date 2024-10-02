from pydantic import BaseModel
from typing import List, Optional

class ArticleBase(BaseModel):
    name: str
    url: str

class ArticleCreate(ArticleBase):
    pass

class Article(ArticleBase):
    id: int
    prediction_id: int

    class Config:
        from_attributes = True

class PredictionBase(BaseModel):
    user_id: int
    predicted_class: str
    confidence: float
    image_url: str
    about: Optional[str] = None
    key_research_topics: Optional[dict] = None
    uses: Optional[str] = None
    illnesses_caused: Optional[str] = None

class PredictionCreate(PredictionBase):
    articles: List[ArticleCreate]

class PredictionRequest(PredictionCreate):
    pass  # You can add any additional fields if needed

class PredictionResponse(PredictionBase):
    id: int
    user_id: int
    articles: List[Article]

    class Config:
        from_attributes = True