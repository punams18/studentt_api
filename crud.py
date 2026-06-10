from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Student


def create_student(db: Session, student):
    new_student = Student(
        name=student.name,
        email=student.email,
        course=student.course
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


def get_students(db: Session):
    return db.query(Student).all()


def get_student(db: Session, student_id: int):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


def update_student(db: Session, student_id: int, student):
    existing = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    existing.name = student.name
    existing.email = student.email
    existing.course = student.course

    db.commit()
    db.refresh(existing)

    return existing


def delete_student(db: Session, student_id: int):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}