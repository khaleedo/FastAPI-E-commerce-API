from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.utils.exceptions import NotFoundException


class ProductService:
    @staticmethod
    def create_product(db: Session, product: ProductCreate) -> Product:
        db_product = Product(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    
    @staticmethod
    def get_product(db: Session, product_id: int) -> Product:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise NotFoundException("Product not found")
        return product
    
    @staticmethod
    def get_products(db: Session, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[Product]:
        query = db.query(Product)
        if active_only:
            query = query.filter(Product.is_active == True)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_product(db: Session, product_id: int, product_update: ProductUpdate) -> Product:
        product = ProductService.get_product(db, product_id)
        update_data = product_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(product, field, value)
        
        db.commit()
        db.refresh(product)
        return product
    
    @staticmethod
    def delete_product(db: Session, product_id: int) -> Product:
        product = ProductService.get_product(db, product_id)
        product.is_active = False
        db.commit()
        return product