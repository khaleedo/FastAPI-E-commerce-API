from typing import List
from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.models.user import User, UserRole
from app.schemas.order import OrderCreate, OrderUpdate
from app.utils.exceptions import NotFoundException, BadRequestException, PermissionException
from decimal import Decimal


class OrderService:
    @staticmethod
    def create_order(db: Session, order: OrderCreate, customer: User) -> Order:
        if not order.items:
            raise BadRequestException("Order must contain at least one item")
        
        # Validate products and calculate total
        total_amount = Decimal('0')
        order_items = []
        
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product or not product.is_active:
                raise BadRequestException(f"Product with id {item.product_id} not found or inactive")
            
            if product.stock_quantity < item.quantity:
                raise BadRequestException(f"Insufficient stock for product {product.name}")
            
            item_total = product.price * item.quantity
            total_amount += item_total
            
            order_items.append(OrderItem(
                product_id=item.product_id,
                quantity=item.quantity,
                price=product.price
            ))
        
        # Create order
        db_order = Order(
            customer_id=customer.id,
            total_amount=total_amount,
            shipping_address=order.shipping_address,
            order_items=order_items
        )
        
        # Update stock quantities
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            product.stock_quantity -= item.quantity
        
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order
    
    @staticmethod
    def get_order(db: Session, order_id: int, user: User) -> Order:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise NotFoundException("Order not found")
        
        # Check permissions
        if user.role != UserRole.ADMIN and order.customer_id != user.id:
            raise PermissionException("Access denied")
        
        return order
    
    @staticmethod
    def get_user_orders(db: Session, user: User, skip: int = 0, limit: int = 100) -> List[Order]:
        return db.query(Order).filter(Order.customer_id == user.id).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_all_orders(db: Session, skip: int = 0, limit: int = 100) -> List[Order]:
        return db.query(Order).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_order_status(db: Session, order_id: int, order_update: OrderUpdate, user: User) -> Order:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise NotFoundException("Order not found")
        
        # Only admins can update order status
        if user.role != UserRole.ADMIN:
            raise PermissionException("Only admins can update order status")
        
        update_data = order_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(order, field, value)
        
        db.commit()
        db.refresh(order)
        return order