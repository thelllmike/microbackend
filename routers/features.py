from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.feature import FeatureCreate, FeatureResponse
from crud.feature import create_feature, get_features, get_feature, update_feature, delete_feature
from database import get_db
from typing import List

router = APIRouter()

# Create a new feature with user_id from frontend
@router.post("/features/", response_model=FeatureResponse)
def create_new_feature(
    feature: FeatureCreate, 
    db: Session = Depends(get_db)
):
    return create_feature(db=db, feature=feature)

@router.get("/features/", response_model=List[FeatureResponse])
def read_features(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_features(db=db, skip=skip, limit=limit)

@router.get("/features/{feature_id}", response_model=FeatureResponse)
def read_feature(feature_id: int, db: Session = Depends(get_db)):
    db_feature = get_feature(db=db, feature_id=feature_id)
    if db_feature is None:
        raise HTTPException(status_code=404, detail="Feature not found")
    return db_feature

@router.put("/features/{feature_id}", response_model=FeatureResponse)
def update_feature_data(feature_id: int, feature: FeatureCreate, db: Session = Depends(get_db)):
    return update_feature(db=db, feature_id=feature_id, feature=feature)

@router.delete("/features/{feature_id}", response_model=FeatureResponse)
def delete_feature_data(feature_id: int, db: Session = Depends(get_db)):
    db_feature = delete_feature(db=db, feature_id=feature_id)
    if db_feature is None:
        raise HTTPException(status_code=404, detail="Feature not found")
    return db_feature