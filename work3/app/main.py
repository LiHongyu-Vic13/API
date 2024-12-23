from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import get_db, SessionLocal
from typing import List
from dotenv import load_dotenv
load_dotenv()
from .database import init_db
init_db()


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)

@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    if not crud.delete_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    return {}

@app.get("/students/", response_model=List[schemas.Student])
def read_students(db: Session = Depends(get_db)):
    return crud.get_students(db)

@app.post("/groups/", response_model=schemas.Group)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    return crud.create_group(db, group)

@app.get("/groups/{group_id}", response_model=schemas.Group)
def read_group(group_id: int, db: Session = Depends(get_db)):
    group = crud.get_group(db, group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@app.delete("/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    if not crud.delete_group(db, group_id):
        raise HTTPException(status_code=404, detail="Group not found")
    return {}

@app.get("/groups/", response_model=List[schemas.Group])
def read_groups(db: Session = Depends(get_db)):
    return crud.get_groups(db)

@app.post("/students/{student_id}/groups/{group_id}")
def add_student_to_group(student_id: int, group_id: int, db: Session = Depends(get_db)):
    if not crud.add_student_to_group(db, student_id, group_id):
        raise HTTPException(status_code=404, detail="Student or Group not found")
    return {"message": "Student added to group"}

@app.post("/students/{student_id}/remove-group")
def remove_student_from_group(student_id: int, db: Session = Depends(get_db)):
    if not crud.remove_student_from_group(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student removed from group"}

@app.get("/groups/{group_id}/students", response_model=List[schemas.Student])
def get_students_in_group(group_id: int, db: Session = Depends(get_db)):
    students = crud.get_students_in_group(db, group_id)
    if not students:
        raise HTTPException(status_code=404, detail="No students found in group")
    return students

@app.post("/students/{student_id}/transfer/{new_group_id}")
def transfer_student(student_id: int, new_group_id: int, db: Session = Depends(get_db)):
    if not crud.transfer_student(db, student_id, new_group_id):
        raise HTTPException(status_code=404, detail="Student or New Group not found")
    return {"message": "Student transferred to new group"}