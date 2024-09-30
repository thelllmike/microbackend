# routers/predict.py
import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile ,Form
from sqlalchemy.orm import Session
from database import get_db
from crud.predict import create_prediction, get_prediction_by_id, get_predictions_by_user_id, update_prediction, delete_prediction
from models.predict import Prediction
from schemas.predict import Article, PredictionRequest, PredictionResponse

router = APIRouter()

@router.post("/details/predictions/", response_model=PredictionResponse)
async def create_new_prediction(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):
    try:
        # Handling 'articles' and ensuring it’s a list of Article dictionaries
        articles_list = request.articles

        # Convert Article objects to dictionaries if they aren't already
        if isinstance(articles_list, str):
            try:
                articles_list = json.loads(articles_list)  # Convert JSON string to list of dictionaries
            except json.JSONDecodeError:
                raise HTTPException(status_code=422, detail="Invalid JSON format for articles")
        
        # Ensuring all items are valid dictionaries for Article
        articles_objects = [Article(**article) if isinstance(article, dict) else article for article in articles_list]

        # Handling 'key_research_topics' similarly
        key_research_topics_list = request.key_research_topics
        if isinstance(key_research_topics_list, str):
            try:
                key_research_topics_list = json.loads(key_research_topics_list)  # Convert JSON string to list
            except json.JSONDecodeError:
                raise HTTPException(status_code=422, detail="Invalid JSON format for key_research_topics")

        # Create the prediction entry in the database
        prediction = create_prediction(
            db=db,
            user_id=request.user_id,
            predicted_class=request.predicted_class,
            confidence=request.confidence,
            image_url=request.image_url,
            about=request.about,
            articles=[article.dict() for article in articles_objects],  # Convert Article objects to dicts
            key_research_topics=key_research_topics_list,
            uses=request.uses,
            illnesses_caused=request.illnesses_caused
        )

        # Return the serialized response
        return {
            "predicted_class": prediction.predicted_class,
            "confidence": prediction.confidence,
            "image_url": prediction.image_url,
            "about": prediction.about,
            "articles": [article.dict() for article in articles_objects],  # Ensure articles are dictionaries
            "key_research_topics": key_research_topics_list,
            "uses": prediction.uses,
            "illnesses_caused": prediction.illnesses_caused
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Utility function to convert Prediction object to dict
def serialize_prediction(prediction: Prediction) -> dict:
    return {
        "id": prediction.id,
        "user_id": prediction.user_id,
        "predicted_class": prediction.predicted_class,
        "confidence": prediction.confidence,
        "image_url": prediction.image_url,
        "about": prediction.about,
        "articles": [Article(**article).dict() if isinstance(article, dict) else article for article in prediction.articles or []],
        "key_research_topics": prediction.key_research_topics or [],
        "uses": prediction.uses,
        "illnesses_caused": prediction.illnesses_caused,
        "created_at": prediction.created_at,
        "updated_at": prediction.updated_at
    }

@router.get("/predictions/{prediction_id}", response_model=dict)
def read_prediction(prediction_id: int, db: Session = Depends(get_db)):
    try:
        prediction = get_prediction_by_id(db, prediction_id)
        if not prediction:
            raise HTTPException(status_code=404, detail="Prediction not found")
        return {"data": serialize_prediction(prediction)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/predictions/user/{user_id}", response_model=dict)
def read_predictions_by_user(user_id: int, db: Session = Depends(get_db)):
    try:
        predictions = get_predictions_by_user_id(db, user_id)
        serialized_predictions = [serialize_prediction(pred) for pred in predictions]
        return {"data": serialized_predictions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/predictions/{prediction_id}", response_model=dict)
def update_existing_prediction(prediction_id: int, data: dict, db: Session = Depends(get_db)):
    try:
        updated_prediction = update_prediction(db, prediction_id, **data)
        if updated_prediction is None:
            raise HTTPException(status_code=404, detail="Prediction not found")
        return {"message": "Prediction updated", "data": serialize_prediction(updated_prediction)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/predictions/{prediction_id}", response_model=dict)
def delete_existing_prediction(prediction_id: int, db: Session = Depends(get_db)):
    try:
        deleted_prediction = delete_prediction(db, prediction_id)
        if deleted_prediction is None:
            raise HTTPException(status_code=404, detail="Prediction not found")
        return {"message": "Prediction deleted", "data": serialize_prediction(deleted_prediction)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))