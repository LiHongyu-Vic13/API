from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..crud.user import get_user_by_email
from ..schemas.user import UserUpdate
from .jwt import get_current_user
from .jwt import get_current_active_user, verify_token
from ..database.database import SessionLocal
from redis import Redis
from ..crud import user as crud_user
from ..schemas.user import User, Token
from ..database.database import get_db
from ..database.models import History
from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserUpdate
from ..crud.user import get_user_by_email, update_user
import redis
from pydantic import BaseModel
import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.history import History


router = APIRouter()
redis_client = redis.Redis.from_url("redis://localhost:6379/0")
#redis = Redis.from_url(os.getenv("REDIS_URL"))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@router.put("/user/update", response_model=UserUpdate)
def update_user_me(user_update: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.email != user_update.email:
        existing_user = get_user_by_email(db, email=user_update.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    update_user(db, user=current_user, email=user_update.email, password=user_update.password)
    return user_update

@router.get("/user/history", response_model=list[History])
def read_user_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 假设每个用户有一个 'history' 关联对象，它是一个包含历史记录的列表
    history = current_user.history
    # 将 SQLAlchemy 对象转换为 Pydantic 模型
    history_list = [History(**item.__dict__) for item in history]
    return history_list

@router.post("/logout")
def logout(refresh_token: str, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    # 检查 refresh token 是否存在于 Redis 中
    if redis_client.exists(refresh_token):
        # 使 refresh token 失效
        redis_client.delete(refresh_token)
        return {"message": "Logged out"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Refresh token not found")
    
