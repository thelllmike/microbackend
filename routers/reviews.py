from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from crud import review as crud_review
from schemas.review import Review, ReviewCreate, ReviewUpdate
from database import get_db

router = APIRouter()

# Create a new review
@router.post("/reviews/", response_model=Review)
def create_new_review(review: ReviewCreate, db: Session = Depends(get_db)):
    return crud_review.create_review(db=db, review=review)

# Get all reviews
@router.get("/reviews/", response_model=List[Review])
def read_reviews(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_review.get_reviews(db=db, skip=skip, limit=limit)

# Get a review by ID
@router.get("/reviews/{review_id}", response_model=Review)
def read_review(review_id: int, db: Session = Depends(get_db)):
    db_review = crud_review.get_review(db=db, review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

# Update a review by ID
@router.put("/reviews/{review_id}", response_model=Review)
def update_review(review_id: int, review: ReviewUpdate, db: Session = Depends(get_db)):
    db_review = crud_review.update_review(db=db, review_id=review_id, review=review)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

# Delete a review by ID
@router.delete("/reviews/{review_id}", response_model=Review)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = crud_review.delete_review(db=db, review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review