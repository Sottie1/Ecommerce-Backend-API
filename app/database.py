from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.models import Base
from fastapi import APIRouter, Depends
from app import schemas, models
from sqlalchemy.orm import Session
import environ

env = environ.Env()
env.read_env()




router = APIRouter()

SQLALCHEMY_DATABASE_URL = env("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

