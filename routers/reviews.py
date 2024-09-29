# app/routers/review.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.review import ReviewSchema
from crud.review import create_review, get_reviews, get_review_by_id, update_review, delete_review
from database import get_db
from utils.auth import get_current_user  # Import the token verification function

router = APIRouter()

# Secure the route for adding a review, the user must be authenticated
@router.post("/reviews/")
def add_review(review: ReviewSchema, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return create_review(db, review, current_user.user_id)

# Secure the route for reading reviews (can allow public access or restrict based on use case)
@router.get("/reviews/")
def read_reviews(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reviews = get_reviews(db, skip=skip, limit=limit)
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found")
    return reviews

# Secure the route for reading a specific review (can allow public access or restrict based on use case)
@router.get("/reviews/{review_id}")
def read_review(review_id: int, db: Session = Depends(get_db)):
    review = get_review_by_id(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

# Secure the route for updating a review, the user must be authenticated
@router.put("/reviews/{review_id}")
def update_review_endpoint(review_id: int, review: ReviewSchema, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    updated_review = update_review(db, review_id, review)
    if not updated_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return updated_review

# Secure the route for deleting a review, the user must be authenticated
@router.delete("/reviews/{review_id}")
def delete_review_endpoint(review_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    deleted_review = delete_review(db, review_id)
    if not deleted_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"detail": "Review deleted"}
