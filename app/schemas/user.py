from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    member = "member"

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    role: UserRole = UserRole.member
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: UserRole

    class Config:
        from_attributes = True    