from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from .category import CategoryResponse


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100,
                      description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., gt=0, description="Product price(must be greater than 0)")
    category_id: int = Field(..., description="Category ID")
    image_url: Optional[str] = Field(None, description="Product image URL")


class ProductCreate(ProductBase):
    pass


class ProductResponse(BaseModel):
    id: int = Field(..., description="Product ID")
    name: str
    description: Optional[str]
    price: float
    category_id: int
    image_url: Optional[str]
    created_at: datetime
    category: CategoryResponse = Field(..., description="Product category details")


    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    products: list[ProductResponse]
    total: int = Field(..., description="Total number of products")


class CartItem(BaseModel):
    product_id: int
    name: str = Field(..., description="Product name")
    price: float = Field(..., description="Product price")
    quantity: int = Field(..., description="Quantity in cart")
    subtotal: float = Field(...,
                            description="Total price for this item(price * quantity)")
    image_url: Optional[str] = Field(None, description="Product image URL")


class CartResponse(BaseModel):
    items: list[CartItem] = Field(..., description="List of items in cart")
    total: float = Field(..., description="Total cart price")
    items_count: int = Field(..., description="Total number of items in cart")



















