from sqlalchemy.orm import Session
from models.predict import Prediction, Article
from schemas.predict import PredictionCreate, ArticleCreate

def create_prediction(db: Session, prediction_data: PredictionCreate):
    # Create a new Prediction object
    prediction = Prediction(
        user_id=1,  # Assuming the user_id comes from some logic
        predicted_class=prediction_data.predicted_class,
        confidence=prediction_data.confidence,
        image_url=prediction_data.image_url,
        about=prediction_data.about,
        key_research_topics=prediction_data.key_research_topics,
        uses=prediction_data.uses,
        illnesses_caused=prediction_data.illnesses_caused
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    # Create Article objects and link them to the prediction
    for article_data in prediction_data.articles:
        article = Article(
            name=article_data.name,
            url=article_data.url,
            prediction_id=prediction.id
        )
        db.add(article)
    
    db.commit()
    return prediction


def get_predictions_by_user_id(db: Session, user_id: int):
    return db.query(Prediction).filter(Prediction.user_id == user_id).all()


def get_prediction_by_id(db: Session, prediction_id: int):
    return db.query(Prediction).filter(Prediction.id == prediction_id).first()

def delete_prediction_by_id(db: Session, prediction_id: int):
    # Retrieve the prediction to be deleted
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()

    # If the prediction doesn't exist, return None
    if not prediction:
        return None

    # Delete all associated articles
    db.query(Article).filter(Article.prediction_id == prediction_id).delete()

    # Delete the prediction
    db.delete(prediction)
    db.commit()
    
    return prediction