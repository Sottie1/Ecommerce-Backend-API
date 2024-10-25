from fastapi import APIRouter
import requests
from fastapi import Depends, HTTPException
from app.schemas import OrderCreate
from app.models import Order, OrderItem, Product, User
from app.dependency import get_db
from sqlalchemy.orm import Session
import httpx
from environs import Env


env = Env()
env.read_env()
router = APIRouter()


@router.post("/api/v1/orders")
def create_order(order: OrderCreate, user_id: int, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create the order
    new_order = Order(user_id=user_id, total=order.total, status="pending")
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Add items to the order
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        order_item = OrderItem(order_id=new_order.id, product_id=product.id, quantity=item.quantity)
        db.add(order_item)
    
    db.commit()

    return {"order_id": new_order.id, "status": new_order.status, "total": new_order.total}


@router.get("/api/v1/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    items = []
    for item in order_items:
        items.append({"product_id": item.product_id, "quantity": item.quantity})
    
    return {"order_id": order.id, "status": order.status, "total": order.total, "items": items}


@router.post("/api/v1/checkout")
async def initiate_payment(order_id: int, user_id: int, db: Session = Depends(get_db)):
    # Retrieve the order from the database
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Calculate total amount in pesewas (GHS * 100)
    total_amount_in_pesewas = int(order.total * 100)
    
    # Retrieve the user's email from the database
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Paystack API key stored in environment variable
    paystack_secret_key = env("PAYSTACK_SECRET_KEY")
    headers = {
        "Authorization": f"Bearer {paystack_secret_key}",
        "Content-Type": "application/json"
    }
    
    # Payload for initializing the transaction
    data = {
        "email": user.email,  # Dynamic user email
        "amount": total_amount_in_pesewas,  
        "currency": "GHS",
        "channels": ["card", "mobile_money", "bank_transfer"]
    }
    
    # Send asynchronous request to Paystack
    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.paystack.co/transaction/initialize", headers=headers, json=data)
    
    # Check if the request was successful
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    
    return response.json()