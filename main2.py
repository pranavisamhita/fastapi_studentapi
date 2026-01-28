from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import SessionLocal
from models import Student

app = FastAPI()

class StudentCreate(BaseModel):
    name: str
    email: str
    age: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/students")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(
        name=student.name,
        email=student.email,
        age=student.age
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()
