from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import SessionLocal
from models import Student

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schema for input
class StudentCreate(BaseModel):
    name: str
    email: str
    age: int

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE student
@app.post("/students")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(name=student.name, email=student.email, age=student.age)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# READ all students
@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

# UPDATE student
@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentCreate, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        return {"error": "Student not found"}
    db_student.name = student.name
    db_student.email = student.email
    db_student.age = student.age
    db.commit()
    db.refresh(db_student)
    return db_student

# DELETE student
@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        return {"error": "Student not found"}
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}
