# app/crud/review.py
from sqlalchemy.orm import Session
from models.review import Review
from schemas.review import ReviewSchema

def create_review(db: Session, review: ReviewSchema, user_id: int):
    db_review = Review(
        user_id=user_id,
        review=review.review,
        rate=review.rate
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_reviews(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Review).offset(skip).limit(limit).all()

def get_review_by_id(db: Session, review_id: int):
    return db.query(Review).filter(Review.id == review_id).first()

def update_review(db: Session, review_id: int, review_data: ReviewSchema):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review:
        db_review.review = review_data.review
        db_review.rate = review_data.rate
        db.commit()
        db.refresh(db_review)
        return db_review
    return None

def delete_review(db: Session, review_id: int):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review:
        db.delete(db_review)
        db.commit()
        return db_review
    return None
