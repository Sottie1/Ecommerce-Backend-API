
from fastapi import APIRouter
from app.database import SessionLocal
from app.schemas import ProductCreate
from sqlalchemy.orm import Session
from fastapi import Depends
from app import schemas, models
from app.models import Product
from app.dependency import get_db
from app.decorator import vendor_required, vendor_or_admin_required
from routers.utility import get_current_user

router = APIRouter()

@router.get("/api/v1/products")
def list_products():
    db = SessionLocal()
    products = db.query(Product).all()
    return products


@router.post("/api/v1/products", dependencies=[Depends(vendor_or_admin_required)])
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Create product
    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        vendor_id=current_user['id'] if current_user['role'] == "vendor" else None  # Only associate vendor_id if the user is a vendor
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/api/v1/vendor/products", dependencies=[Depends(vendor_required)])
def get_vendor_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(models.Product.vendor_id == get_current_user.id).all()
    return products
