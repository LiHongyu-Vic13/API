from fastapi import Depends, HTTPException, Security
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer
from . import models, schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Функции зависимостей для получения сеансов базы данных
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = db.query(models.User).filter(models.User.username == "some_username").first()
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid authentication token")
    return user