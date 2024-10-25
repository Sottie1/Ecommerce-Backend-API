# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List

from app.models import UserRole

# Pydantic Schema for Product Creation
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class User(BaseModel):
    id: int
    username: str
    email: EmailStr

# Pydantic Schema for User Creation
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = UserRole.CUSTOMER

# Pydantic Schema for User Response
class UserResponse(BaseModel):
    username: str
    email: EmailStr

# Pydantic Schema for Cart Item Creation
class CartItemCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int

# Pydantic Schema for Order Creation
class OrderCreate(BaseModel):
    user_id: int
    total: float

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    total: float

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str