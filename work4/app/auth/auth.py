from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..crud.user import get_user_by_email, create_user
from ..schemas.user import Token
from jose import jwt
from .jwt import create_access_token, create_refresh_token
from .. import database
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import timedelta
from ..database.database import get_db
from ..schemas.user import User, Token
from .jwt import create_access_token, create_refresh_token, verify_token
from app.settings import settings
import redis
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
redis_client = redis.Redis.from_url("redis://localhost:6379/0")

router = APIRouter()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

@router.post("/register", response_model=Token)
def register_user(email: str, password: str, db: Session = Depends(get_db)):
    if get_user_by_email(db, email=email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = create_user(db, email=email, password=password)
    access_token_expires = 3600
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(seconds=access_token_expires))
    refresh_token = create_refresh_token(data={"sub": user.email})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=form_data.username)
    if not user or not user.check_password(form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token_expires = 3600
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(seconds=access_token_expires))
    refresh_token = create_refresh_token(data={"sub": user.email})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=form_data.username)
    if not user or not user.check_password(form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"sub": user.email})
    return {"access_token": access_token, "refresh_token": refresh_token}