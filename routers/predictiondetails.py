from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from crud.predict import create_prediction, delete_prediction_by_id, get_most_recent_prediction, get_prediction_by_id, get_predictions_by_user_id, get_recent_predictions_by_user_id
from schemas.predict import PredictionRequest, PredictionResponse

router = APIRouter()

@router.post("/details/predictions/", response_model=PredictionResponse)
async def create_new_prediction(request: PredictionRequest, db: Session = Depends(get_db)):
    try:
        # Create the prediction entry in the database
        prediction = create_prediction(db=db, prediction_data=request)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/predictions/{prediction_id}", response_model=PredictionResponse)
def read_prediction(prediction_id: int, db: Session = Depends(get_db)):
    prediction = get_prediction_by_id(db, prediction_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction

@router.delete("/predictions/{prediction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prediction(prediction_id: int, db: Session = Depends(get_db)):
    prediction = delete_prediction_by_id(db, prediction_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return None

# Fetch all predictions for a user by user_id
@router.get("/predictions/user/{user_id}", response_model=List[PredictionResponse])
def read_user_predictions(user_id: int, db: Session = Depends(get_db)):
    predictions = get_predictions_by_user_id(db, user_id)
    if not predictions:
        raise HTTPException(status_code=404, detail="No predictions found for this user")
    return predictions

# Fetch the 5 most recent predictions for a user by user_id
@router.get("/predictions/userrecent/{user_id}", response_model=List[PredictionResponse])
def read_recent_predictions(user_id: int, db: Session = Depends(get_db), limit: int = 5):
    predictions = get_recent_predictions_by_user_id(db, user_id, limit)
    if not predictions:
        raise HTTPException(status_code=404, detail="No recent predictions found for this user")
    return predictions