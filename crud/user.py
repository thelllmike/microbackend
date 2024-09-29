# app/crud/user.py
from datetime import datetime
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserUpdate
from utils.auth import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()  # Use user_id if your model has it

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)  # Make sure to import get_password_hash from utils.auth
    db_user = User(
        email=user.email, 
        hashed_password=hashed_password, 
        first_name=user.first_name, 
        last_name=user.last_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        if user_update.password:
            db_user.hashed_password = get_password_hash(user_update.password)
        if user_update.first_name:
            db_user.first_name = user_update.first_name
        if user_update.last_name:
            db_user.last_name = user_update.last_name
        if user_update.email:
            db_user.email = user_update.email
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def update_user_otp(db: Session, email: str, otp: str):
    user = get_user_by_email(db, email)
    if user:
        user.otp = otp
        user.otp_created_at = datetime.utcnow()
        db.commit()

def update_user_password(db: Session, email: str, hashed_password: str):
    user = get_user_by_email(db, email)
    if user:
        user.hashed_password = hashed_password
        user.otp = None  # Clear OTP after password reset
        user.otp_created_at = None
        db.commit()
