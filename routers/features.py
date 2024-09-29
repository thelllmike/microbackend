from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.feature import FeatureSchema
from crud.feature import create_feature, get_features, get_feature, update_feature, delete_feature
from database import get_db

router = APIRouter()

@router.post("/features/")
def create_new_feature(feature: FeatureSchema, db: Session = Depends(get_db), name: str = "LoggedInUser", email: str = "user@example.com", user_id: int = 1):  # Add user_id
    return create_feature(db=db, feature=feature, name=name, email=email, user_id=user_id)

@router.get("/features/")
def read_features(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_features(db=db, skip=skip, limit=limit)

@router.get("/features/{feature_id}")
def read_feature(feature_id: int, db: Session = Depends(get_db)):
    db_feature = get_feature(db=db, feature_id=feature_id)
    if db_feature is None:
        raise HTTPException(status_code=404, detail="Feature not found")
    return db_feature

@router.put("/features/{feature_id}")
def update_feature_data(feature_id: int, feature: FeatureSchema, db: Session = Depends(get_db)):
    return update_feature(db=db, feature_id=feature_id, feature=feature)

@router.delete("/features/{feature_id}")
def delete_feature_data(feature_id: int, db: Session = Depends(get_db)):
    db_feature = delete_feature(db=db, feature_id=feature_id)
    if db_feature is None:
        raise HTTPException(status_code=404, detail="Feature not found")
    return db_feature
