# backend/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List, Optional

class StudentBase(BaseModel):
    learning_style: str
    preferred_subjects: Dict[str, str]
    interests: List[str]
    academic_level: Dict[str, str]

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    student_id: int
    profile_creation_date: datetime
    last_modified_date: datetime

    class Config:
        orm_mode = True
        
# USer Schemas
class UserCreate(BaseModel):
    email: str
    password: str


class User(BaseModel):
    id: int
    email: str
    is_active: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None