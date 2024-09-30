# routers/predict.py
import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile ,Form
from sqlalchemy.orm import Session
from database import get_db
from crud.predict import create_prediction, get_prediction_by_id, get_predictions_by_user_id, update_prediction, delete_prediction
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

@router.get("/predictions/{prediction_id}", response_model=dict)
def read_prediction(prediction_id: int, db: Session = Depends(get_db)):
    prediction = get_prediction_by_id(db, prediction_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return {"data": prediction}

@router.get("/predictions/user/{user_id}", response_model=dict)
def read_predictions_by_user(user_id: int, db: Session = Depends(get_db)):
    predictions = get_predictions_by_user_id(db, user_id)
    return {"data": predictions}

@router.put("/predictions/{prediction_id}", response_model=dict)
def update_existing_prediction(prediction_id: int, data: dict, db: Session = Depends(get_db)):
    updated_prediction = update_prediction(db, prediction_id, **data)
    if updated_prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return {"message": "Prediction updated", "data": updated_prediction}

@router.delete("/predictions/{prediction_id}", response_model=dict)
def delete_existing_prediction(prediction_id: int, db: Session = Depends(get_db)):
    deleted_prediction = delete_prediction(db, prediction_id)
    if deleted_prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return {"message": "Prediction deleted", "data": deleted_prediction}