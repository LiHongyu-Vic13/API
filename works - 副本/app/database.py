from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

# Получение URL базы данных из переменных среды
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

# Создание движка SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создание базового класса для наследования всех моделей
Base = declarative_base()

# Создание класса SessionLocal, который будет использоваться для создания новой сессии базы данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Предоставляет объект сеанса глобальной базы данных
db_session = None

def init_db():
    """初始化数据库：创建所有表"""
    Base.metadata.create_all(bind=engine)

# Предоставляет функцию зависимости для создания или получения сеанса базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Определение модели базы данных
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship("Group", back_populates="students")

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    students = relationship("Student", back_populates="group")