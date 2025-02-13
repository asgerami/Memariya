from sqlalchemy import create_engine,Column, Integer,String, JSON, DateTime 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "postgresql://memarya_user:02121994@localhost:5432/memarya_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Student(Base):
    __tablename__= "students"

    student_id = Column(Integer, primary_key=True, index=True)
    learning_style = Column(String)
    preferred_subjects = Column(JSON)
    interests = Column(JSON)
    academic_level = Column(JSON)
    profile_creation_date = Column(DateTime, default=datetime.utcnow)
    last_modified_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    Base.metadata.create_all(bind=engine)
