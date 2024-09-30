# crud/predict.py
import json
from sqlalchemy.orm import Session
from models.predict import Prediction

# Create a new prediction
def create_prediction(db: Session, user_id: int, predicted_class: str, confidence: float, image_url: str, about: str, articles: list, key_research_topics: list, uses: str, illnesses_caused: str):
    db_prediction = Prediction(
        user_id=user_id,
        predicted_class=predicted_class,
        confidence=confidence,
        image_url=image_url,
        about=about,
        articles=json.dumps(articles),  # Store as JSON string
        key_research_topics=json.dumps(key_research_topics),  # Store as JSON string
        uses=uses,
        illnesses_caused=illnesses_caused,
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

# Retrieve a prediction by ID
def get_prediction_by_id(db: Session, prediction_id: int):
    return db.query(Prediction).filter(Prediction.id == prediction_id).first()

# Retrieve all predictions by user ID
def get_predictions_by_user_id(db: Session, user_id: int):
    return db.query(Prediction).filter(Prediction.user_id == user_id).all()

# Update an existing prediction
def update_prediction(db: Session, prediction_id: int, user_id: int = None, predicted_class: str = None, 
                      confidence: float = None, image_url: str = None, about: str = None, articles: list = None, 
                      key_research_topics: list = None, uses: str = None, illnesses_caused: str = None):
    
    db_prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    
    if db_prediction is None:
        return None  # Or raise an exception if preferred

    if user_id is not None:
        db_prediction.user_id = user_id
    if predicted_class is not None:
        db_prediction.predicted_class = predicted_class
    if confidence is not None:
        db_prediction.confidence = confidence
    if image_url is not None:
        db_prediction.image_url = image_url
    if about is not None:
        db_prediction.about = about
    if articles is not None:
        db_prediction.articles = json.dumps(articles)  # Convert list to JSON string
    if key_research_topics is not None:
        db_prediction.key_research_topics = json.dumps(key_research_topics)  # Convert list to JSON string
    if uses is not None:
        db_prediction.uses = uses
    if illnesses_caused is not None:
        db_prediction.illnesses_caused = illnesses_caused

    db.commit()
    db.refresh(db_prediction)
    return db_prediction

# Delete a prediction
def delete_prediction(db: Session, prediction_id: int):
    db_prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    
    if db_prediction is None:
        return None  # Or raise an exception if preferred

    db.delete(db_prediction)
    db.commit()
    return db_prediction