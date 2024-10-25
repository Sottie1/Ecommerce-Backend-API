from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from routers.utility import get_current_user
from app.models import User
   

def admin_required(current_user: dict = Depends(get_current_user)):
    if current_user['role'] != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user


def vendor_required(current_user: dict = Depends(get_current_user)):
    if current_user['role'] != "vendor":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

def vendor_or_admin_required(current_user: dict = Depends(get_current_user)):
    if current_user['role'] not in ["vendor", "admin"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user
