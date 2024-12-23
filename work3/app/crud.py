from sqlalchemy.orm import Session
from . import models, schemas

# CRUD operations for Students

def get_student(db: Session, student_id: int):
    """Получение информации об отдельных студентах"""
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_students(db: Session):
    """Получить информацию для всех студентов"""
    return db.query(models.Student).all()

def create_student(db: Session, student: schemas.StudentCreate):
    """Создание нового ученика"""
    db_student = models.Student(name=student.name)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    """Удаление учащегося"""
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student:
        db.delete(student)
        db.commit()
        return True
    return False

# CRUD operations for Groups

def get_group(db: Session, group_id: int):
    """Получение информации для одной группы учащихся"""
    return db.query(models.Group).filter(models.Group.id == group_id).first()

def get_groups(db: Session):
    """Получить информацию по всем студенческим группам"""
    return db.query(models.Group).all()

def create_group(db: Session, group: schemas.GroupCreate):
    """Создание новой студенческой группы"""
    db_group = models.Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def delete_group(db: Session, group_id: int):
    """Удаление группы учащихся"""
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if group:
        db.delete(group)
        db.commit()
        return True
    return False

# Additional operations

def add_student_to_group(db: Session, student_id: int, group_id: int):
    """Добавление учащихся в группу учащихся"""
    student = get_student(db, student_id)
    group = get_group(db, group_id)
    if student and group:
        student.group_id = group.id
        db.commit()
        return True
    return False

def remove_student_from_group(db: Session, student_id: int):
    """Удаление учащегося из группы учащихся"""
    student = get_student(db, student_id)
    if student:
        student.group_id = None
        db.commit()
        return True
    return False

def get_students_in_group(db: Session, group_id: int):
    """Соберите всех учащихся в студенческую группу"""
    group = get_group(db, group_id)
    if group:
        return db.query(models.Student).filter(models.Student.group_id == group.id).all()
    return []

def transfer_student(db: Session, student_id: int, new_group_id: int):
    """Перевод учащихся из одной группы в другую"""
    student = get_student(db, student_id)
    if student:
        student.group_id = new_group_id
        db.commit()
        return True
    return False

from sqlalchemy.orm import Session
from . import models, schemas

def get_user_by_token(db: Session, token: str):
    # 根据token获取用户
    # 这里需要实现具体的逻辑
    return models.User()