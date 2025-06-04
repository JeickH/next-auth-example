from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.user import Token, User, UserCreate, LoginRequest
from app.core.security import (
    create_access_token,
    authenticate_user,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.services import user as user_service

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=User)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )
    return user_service.create_user(db=db, user=user_in)

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
