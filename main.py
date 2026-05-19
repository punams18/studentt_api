'''from fastapi import FastAPI

app = FastAPI()


def create_admin_if_not_exists():
     print("Admin check running...")


@app.on_event("startup")
def startup():
    create_admin_if_not_exists()



from database import SessionLocal, engine, Base

from fastapi import FastAPI
from database import SessionLocal, engine
from models import User
from auth import hash_password
from database import Base

app = FastAPI()


# 👇 PASTE HERE
def create_admin_if_not_exists():
    db = SessionLocal()
    
    admin = db.query(User).filter(User.username == "admin").first()
    
    if not admin:
        new_admin = User(
            username="admin",
            password=hash_password("admin123")
        )
        db.add(new_admin)
        db.commit()
    
    db.close()


# 👇 startup function
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    create_admin_if_not_exists()
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from database import SessionLocal, engine
from models import Base, Admin
import crud
import schemas
from auth import (
    hash_password,
    verify_password,
    create_access_token
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

security = HTTPBearer()

# Create DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dummy admin create
@app.on_event("startup")
def create_admin():
    db = SessionLocal()

    admin = db.query(Admin).filter(
        Admin.username == "admin"
    ).first()

    if not admin:
        new_admin = Admin(
            username="admin",
            password=hash_password("admin123")
        )

        db.add(new_admin)
        db.commit()

    db.close()


# Token verification
def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return credentials.credentials


# LOGIN API
@app.post("/login")
def login(data: schemas.LoginSchema,
          db: Session = Depends(get_db)):

    admin = db.query(Admin).filter(
        Admin.username == data.username
    ).first()

    if not admin:
        raise HTTPException(
            status_code=401,
            detail="Invalid username"
        )

    if not verify_password(
        data.password,
        admin.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    token = create_access_token(
        {"sub": admin.username}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# CREATE STUDENT
@app.post("/students")
def add_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    token: str = Depends(verify_token)
):
    return crud.create_student(db, student)


# GET ALL STUDENTS
@app.get("/students")
def all_students(
    db: Session = Depends(get_db),
    token: str = Depends(verify_token)
):
    return crud.get_students(db)


# GET SINGLE STUDENT
@app.get("/students/{id}")
def single_student(
    id: int,
    db: Session = Depends(get_db),
    token: str = Depends(verify_token)
):
    return crud.get_student(db, id)


# UPDATE STUDENT
@app.put("/students/{id}")
def update_student(
    id: int,
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    token: str = Depends(verify_token)
):
    return crud.update_student(
        db,
        id,
        student
    )


# DELETE STUDENT
@app.delete("/students/{id}")
def delete_student(
    id: int,
    db: Session = Depends(get_db),
    token: str = Depends(verify_token)
):
    crud.delete_student(db, id)

    return {
        "message": "Student deleted"
    }

from sqlalchemy.orm import Session

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    create_admin_if_not_exists()



from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    # create_admin_if_not_exists()  ❌ remove this


    def create_admin_if_not_exists():
    print("Admin check running...")
    # later you can add DB logic here

    from fastapi import FastAPI

app = FastAPI()


def create_admin_if_not_exists():
    print("Admin check running...")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    create_admin_if_not_exists()'''



from fastapi import FastAPI

app = FastAPI()


def create_admin_if_not_exists():
    print("Admin check running...")


@app.on_event("startup")
def startup():
    create_admin_if_not_exists()


@app.get("/")
def home():
    return {"message": "FastAPI running successfully"}

from fastapi import FastAPI

app = FastAPI()

students = []


@app.post("/students")
def create_student(student: dict):
    students.append(student)
    return {"message": "Student created", "data": student}


@app.get("/students")
def get_students():
    return students


@app.get("/students/{id}")
def get_student(id: int):
    return students[id]


@app.put("/students/{id}")
def update_student(id: int, student: dict):
    students[id] = student
    return {"message": "Student updated"}


@app.delete("/students/{id}")
def delete_student(id: int):
    students.pop(id)
    return {"message": "Student deleted"}