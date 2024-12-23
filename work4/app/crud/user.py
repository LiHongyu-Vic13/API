from sqlalchemy.orm import Session
from ..database.models import User
from .hash import verify_password
from sqlalchemy.orm import Session
from ..models.user import User 
from ..database.models import User

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_user(db: Session, email: str, password: str):
    # 创建新用户并保存到数据库的逻辑
    hashed_password = ...  # 密码哈希逻辑
    new_user = User(email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    return new_user

def update_user(db: Session, user: User, email: str, password: str):
    # 更新用户信息的逻辑
    user.email = email
    user.hashed_password = password  # 假设你已经对密码进行了哈希处理
    db.add(user)
    db.commit()