# backend/main.py
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import models, schemas, utils
from .database import SessionLocal, engine
import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging  # Import logging

# import oauth2
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get("/")  # Add this line to define the root endpoint
async def read_root():
    return {"message": "Hello, world!"}  # Return a simple response


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logging.debug(f"Received user data: {user}")  # Log the incoming user data
    try:
        hashed_password = utils.hash_password(user.password)
        db_user = models.User(email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logging.info(f"Created user with id: {db_user.id}")
        return db_user
    except Exception as e:
        logging.exception(f"Error creating user: {e}")
        db.rollback()  # Rollback the transaction in case of an error
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = utils.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user


@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    logging.debug(f"Received student data: {student}")  # Log the incoming student data
    try:
        db_student = models.Student(**student.dict())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        logging.info(f"Created student with id: {db_student.student_id}")
        return db_student
    except Exception as e:
        logging.exception(f"Error creating student: {e}")
        db.rollback()  # Rollback the transaction in case of an error
        raise HTTPException(status_code=500, detail=str(e))


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
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        explanation = response.text

        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))