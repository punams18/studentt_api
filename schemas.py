from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    email: str
    course: str

class StudentResponse(StudentCreate):
    id: int

    class Config:
        orm_mode = True


class LoginSchema(BaseModel):
    username: str
    password: str