

from fastapi import APIRouter, Depends, HTTPException, status
from app import schemas, models, database
from sqlalchemy.orm import Session
from app.dependency import get_db
from app.models import User, UserRole
from app.decorator import admin_required
from routers.utility import get_current_user



router = APIRouter()

@router.put("/api/v1/users/{user_id}/role")
def update_user_role(user_id: int, role: str, db: Session = Depends(get_db), current_user: dict = Depends(admin_required)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.role = role
    db.commit()
    db.refresh(db_user)
    return db_user



@router.get("/api/v1/users/{user_id}", response_model=schemas.User, dependencies=[Depends(admin_required)])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
