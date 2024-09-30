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
        # Create the prediction entry in the database
        prediction = create_prediction(
            db=db,
            user_id=request.user_id,
            predicted_class=request.predicted_class,
            confidence=request.confidence,
            image_url=request.image_url,
            about=request.about,
            articles=[article.dict() for article in request.articles] if request.articles else [],
            key_research_topics=request.key_research_topics if isinstance(request.key_research_topics, list) else [],
            uses=request.uses,
            illnesses_caused=request.illnesses_caused
        )

        # Ensure proper serialization for response
        return PredictionResponse(
            predicted_class=prediction.predicted_class,
            confidence=prediction.confidence,
            image_url=prediction.image_url,
            about=prediction.about,
            articles=[Article(**article) for article in prediction.articles],
            key_research_topics=prediction.key_research_topics,
            uses=prediction.uses,
            illnesses_caused=prediction.illnesses_caused
        )

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