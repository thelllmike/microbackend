from pydantic import BaseModel

class PredictionRequest(BaseModel):
    user_id: int

class PredictionResponse(BaseModel):
    predicted_class: str
    confidence: float
