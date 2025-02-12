from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine
import google.generativeai as genai  # Import Gemini library
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Load Gemini API key

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@app.get("/content/generate")
def generate_content(concept: str, student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    learning_style = db_student.learning_style
    interests = db_student.interests
    prompt = f"Explain {concept} in a way that is easy for a {learning_style} learner to understand, and link to these interests {interests}."

    genai.configure(api_key=GOOGLE_API_KEY)

    try:
        model = genai.GenerativeModel('gemini-pro')  # Specify the Gemini model
        response = model.generate_content(prompt)
        explanation = response.text

        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))