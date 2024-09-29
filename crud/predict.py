from sqlalchemy.orm import Session
from models.predict import Prediction

def create_prediction(db: Session, user_id: int, predicted_class: str, confidence: float, image_url: str):
    db_prediction = Prediction(user_id=user_id, predicted_class=predicted_class, confidence=confidence, image_url=image_url)
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction
