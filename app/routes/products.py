from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..servicies.product_service import ProductService
from ..schemas.product import ProductResponse, ProductListResponse

router = APIRouter(
    prefix="/api/products",
    tags=["products"]
)

@router.get("", response_model=ProductListResponse, status_code=status.HTTP_200_OK)
def get_products(db: Session = Depends(get_db)):
    service = ProductService(db)  # передаём готовую сессию
    return service.get_all_products()

@router.get("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def get_product(product_id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.ge




