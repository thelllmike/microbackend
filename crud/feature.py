from sqlalchemy.orm import Session
from models.feature import Feature
from schemas.feature import FeatureCreate

def create_feature(db: Session, feature: FeatureCreate):
    db_feature = Feature(
        name=feature.name, 
        email=feature.email, 
        feature=feature.feature, 
        user_id=feature.user_id  # Use user_id from the request body
    )
    db.add(db_feature)
    db.commit()
    db.refresh(db_feature)
    return db_feature

def get_features(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Feature).offset(skip).limit(limit).all()

def get_feature(db: Session, feature_id: int):
    return db.query(Feature).filter(Feature.feature_id == feature_id).first()

def update_feature(db: Session, feature_id: int, feature: FeatureCreate):
    db_feature = db.query(Feature).filter(Feature.feature_id == feature_id).first()
    if db_feature:
        db_feature.feature = feature.feature
        db.commit()
        db.refresh(db_feature)
    return db_feature

def delete_feature(db: Session, feature_id: int):
    db_feature = db.query(Feature).filter(Feature.feature_id == feature_id).first()
    if db_feature:
        db.delete(db_feature)
        db.commit()
    return db_feature