from sqlalchemy.orm import Session
from models.review import Review
from schemas.review import ReviewCreate, ReviewUpdate

# Create a new review
def create_review(db: Session, review: ReviewCreate):
    db_review = Review(
        user_id=review.user_id,
        name=review.name,
        email=review.email,
        review=review.review,
        rate=review.rate,
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# Retrieve all reviews (with optional pagination)
def get_reviews(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Review).offset(skip).limit(limit).all()

# Retrieve a single review by its ID
def get_review(db: Session, review_id: int):
    return db.query(Review).filter(Review.id == review_id).first()

# Update an existing review
def update_review(db: Session, review_id: int, review: ReviewUpdate):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review:
        if review.name is not None:
            db_review.name = review.name
        if review.email is not None:
            db_review.email = review.email
        if review.review is not None:
            db_review.review = review.review
        if review.rate is not None:
            db_review.rate = review.rate
        db.commit()
        db.refresh(db_review)
    return db_review

# Delete a review
def delete_review(db: Session, review_id: int):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review:
        db.delete(db_review)
        db.commit()
    return db_review