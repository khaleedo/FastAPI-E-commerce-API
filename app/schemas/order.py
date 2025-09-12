from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from app.models.order import OrderStatus


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: int
    price: Decimal
    
    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    shipping_address: str


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    shipping_address: Optional[str] = None


class OrderResponse(OrderBase):
    id: int
    customer_id: int
    total_amount: Decimal
    status: OrderStatus
    created_at: datetime
    order_items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True