from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    role: UserRole = UserRole.MEMBER
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