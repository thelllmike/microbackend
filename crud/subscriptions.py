from sqlalchemy.orm import Session
from models.subscriptions import Subscription
from schemas.subscriptions import SubscriptionCreate, SubscriptionUpdate

# Create a new subscription
def create_subscription(db: Session, subscription: SubscriptionCreate):
    db_subscription = Subscription(
        user_id=subscription.user_id,  # Make sure user_id is passed
        subscription_type=subscription.subscription_type,
        billing_frequency=subscription.billing_frequency,
        subscription_plan=subscription.subscription_plan,
        subscription_price=subscription.subscription_price,
        ids_per_month=subscription.ids_per_month,
        savings_percentage=subscription.savings_percentage,
        subscription_end_date=subscription.subscription_end_date,
        free_id_count=subscription.free_id_count,
        purchased_id_count=subscription.purchased_id_count
    )
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

# Get a subscription by ID
def get_subscription(db: Session, subscription_id: int):
    return db.query(Subscription).filter(Subscription.subscription_id == subscription_id).first()

# Get subscriptions by user ID
def get_subscriptions_by_user(db: Session, user_id: int):
    return db.query(Subscription).filter(Subscription.user_id == user_id).all()

# Update a subscription
def update_subscription(db: Session, subscription_id: int, subscription_update: SubscriptionUpdate):
    db_subscription = db.query(Subscription).filter(Subscription.subscription_id == subscription_id).first()
    if db_subscription:
        for key, value in subscription_update.dict(exclude_unset=True).items():
            setattr(db_subscription, key, value)
        db.commit()
        db.refresh(db_subscription)
    return db_subscription

# Delete a subscription
def delete_subscription(db: Session, subscription_id: int):
    db_subscription = db.query(Subscription).filter(Subscription.subscription_id == subscription_id).first()
    if db_subscription:
        db.delete(db_subscription)
        db.commit()
        return True
    return False