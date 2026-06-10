from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import Student
from schemas import StudentCreate, StudentResponse
import crud

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Student API Running Successfully"}


@app.post("/students", response_model=StudentResponse)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    return crud.create_student(db, student)


@app.get("/students")
def get_students(
    db: Session = Depends(get_db)
):
    return crud.get_students(db)


@app.get("/students/{student_id}")
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_student(db, student_id)


@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    return crud.update_student(
        db,
        student_id,
        student
    )


@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    return crud.delete_student(
        db,
        student_id
    )