from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Temporary in-memory storage
students = []

# Data model
class Student(BaseModel):
    name: str
    email: str
    age: int


@app.get("/students")
def get_students():
    return students


@app.post("/students")
def add_student(student: Student):
    students.append(student)
    return {"message": "Student added successfully", "student": student}


@app.put("/students/{index}")
def update_student(index: int, student: Student):
    students[index] = student
    return {"message": "Student updated successfully", "student": student}


@app.delete("/students/{index}")
def delete_student(index: int):
    removed = students.pop(index)
    return {"message": "Student deleted", "student": removed}
