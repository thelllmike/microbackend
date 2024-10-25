from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import subscriptions as crud_subscription
from schemas.subscriptions import SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse
from database import get_db
from typing import List

router = APIRouter()

# Create a subscription
@router.post("/subscriptions/", response_model=SubscriptionResponse)
def create_subscription(subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    return crud_subscription.create_subscription(db, subscription)

# Get a subscription by ID
@router.get("/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
def get_subscription(subscription_id: int, db: Session = Depends(get_db)):
    subscription = crud_subscription.get_subscription(db, subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription

# Get all subscriptions by user ID
@router.get("/subscriptions/user/{user_id}", response_model=List[SubscriptionResponse])
def get_subscriptions_by_user(user_id: int, db: Session = Depends(get_db)):
    return crud_subscription.get_subscriptions_by_user(db, user_id)

# Update a subscription
@router.put("/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
def update_subscription(subscription_id: int, subscription_update: SubscriptionUpdate, db: Session = Depends(get_db)):
    return crud_subscription.update_subscription(db, subscription_id, subscription_update)

# Delete a subscription
@router.delete("/subscriptions/{subscription_id}")
def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    deleted = crud_subscription.delete_subscription(db, subscription_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return {"message": "Subscription deleted"}