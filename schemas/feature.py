from pydantic import BaseModel

class FeatureSchema(BaseModel):
    feature: str
    user_id: int  # Include user_id in schema

    class Config:
        orm_mode = True
