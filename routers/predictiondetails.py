from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from crud.predict import create_prediction, get_prediction_by_id
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