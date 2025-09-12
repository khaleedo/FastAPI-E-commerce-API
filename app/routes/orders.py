from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate
from app.services.order_service import OrderService
from app.dependencies import get_current_active_user, require_admin
from app.models.user import User, UserRole

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new order"""
    return OrderService.create_order(db=db, order=order, customer=current_user)


@router.get("/my-orders", response_model=List[OrderResponse])
def get_my_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get current user's orders"""
    return OrderService.get_user_orders(db=db, user=current_user, skip=skip, limit=limit)


@router.get("/", response_model=List[OrderResponse])
def get_all_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get all orders (Admin only)"""
    return OrderService.get_all_orders(db=db, skip=skip, limit=limit)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific order"""
    return OrderService.get_order(db=db, order_id=order_id, user=current_user)


@router.patch("/{order_id}", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update order status (Admin only)"""
    return OrderService.update_order_status(db=db, order_id=order_id, order_update=order_update, user=current_user)