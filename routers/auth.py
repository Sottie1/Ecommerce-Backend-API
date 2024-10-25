from fastapi import APIRouter, Depends, HTTPException
from app.models import User
from app.database import SessionLocal
from passlib.context import CryptContext
from jose import JWTError, jwt
from app import schemas, models
from app.schemas import UserCreate, UserResponse
from sqlalchemy.orm import Session
from app.dependency import get_db
from routers.utility import hash_password
import environ
router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = environ.Env.read_env('SECRET_KEY')
ALGORITHM = environ.Env.read_env('ALGORITHM')


@router.post("/api/v1/register")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the username or email is already taken
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    # Hash the password
    hashed_password = hash_password(user.password)

    # Create a new user
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,  
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

