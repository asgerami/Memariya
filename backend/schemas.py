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