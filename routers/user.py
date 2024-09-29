from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
from models.user import User
from crud.user import get_user_by_email, create_user, update_user, delete_user, get_user, update_user_otp, update_user_password
from schemas.user import PasswordResetConfirm, PasswordResetRequest, UserCreate, UserUpdate, UserResponse, TokenData
from utils.auth import create_access_token, create_reset_token, generate_otp, get_password_hash, is_otp_valid, verify_password, verify_reset_token
from utils.email import send_otp_email, send_reset_email

router = APIRouter()

# Constants for token expiration and other settings
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create a new user
@router.post("/register/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

# Get user by ID
@router.get("/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Update user by ID
@router.put("/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    updated_user = update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# Delete user by ID
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    deleted_user = delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"ok": True}

# Login Route
@router.post("/login", response_model=TokenData)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, email=form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create an access token with the user email in the subject
    access_token = create_access_token(data={"sub": user.email})
    
    # Return the token, its type, user_id, and first_name
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": user.user_id,
        "first_name": user.first_name  # Include the first name here
    }


@router.post("/password-reset/request/")
def generate_otp_endpoint(payload: PasswordResetRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=payload.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp = generate_otp()  # Generate OTP
    update_user_otp(db, email=payload.email, otp=otp)  # Store OTP
    # send_otp_email(user.email, otp)  # Send OTP via email (implement this)
    return {"msg": "OTP sent to your email"}

# Route for resetting password using OTP
@router.post("/password-reset/confirm/")
def reset_password(payload: PasswordResetConfirm, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=payload.email)
    if not user or user.otp != payload.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP or email")

    if not is_otp_valid(user.otp_created_at):
        raise HTTPException(status_code=400, detail="OTP has expired")

    hashed_password = get_password_hash(payload.new_password)  # Correct usage
    update_user_password(db, email=payload.email, hashed_password=hashed_password)
    return {"msg": "Password successfully reset"}

