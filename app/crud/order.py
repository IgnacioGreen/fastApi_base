from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate, OrderUpdate
from typing import List, Optional

def create_order(db: Session, order: OrderCreate, user_id: int) -> Order:
    # Calcular el total
    total_amount = sum(item.quantity * item.unit_price for item in order.items)
    
    # Crear el pedido
    db_order = Order(
        user_id=user_id,
        status=order.status,
        total_amount=total_amount
    )
    db.add(db_order)
    db.flush()  # Para obtener el ID del pedido
    
    # Crear los items del pedido
    for item in order.items:
        db_item = OrderItem(
            order_id=db_order.id,
            product_name=item.product_name,
            quantity=item.quantity,
            unit_price=item.unit_price
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int) -> Optional[Order]:
    return db.query(Order).filter(Order.id == order_id).first()

def get_user_orders(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
    return db.query(Order).filter(Order.user_id == user_id).offset(skip).limit(limit).all()

def update_order(db: Session, order_id: int, order_update: OrderUpdate) -> Optional[Order]:
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    
    update_data = order_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_order, field, value)
    
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int) -> bool:
    db_order = get_order(db, order_id)
    if not db_order:
        return False
    
    db.delete(db_order)
    db.commit()
    return True 