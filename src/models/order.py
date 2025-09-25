"""
Order class (value object)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import json
from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import relationship
from models.base import Base
from models.order_item import OrderItem

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    
    # Relationship to order items
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    @classmethod
    def from_redis(cls, data: dict):
        obj = cls()
        obj.id = int(data["id"])
        obj.user_id = int(data["user_id"])
        obj.total_amount = float(data["total_amount"])
        raw_items = json.loads(data["items"])
        obj.order_items = [
            OrderItem(product_id=int(item["product_id"]), quantity=int(item["quantity"]))
            for item in raw_items
        ]
        return obj
