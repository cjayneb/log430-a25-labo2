"""
Products (write-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from sqlalchemy import desc
from models.product import Product
from db import get_redis_conn, get_sqlalchemy_session
from queries.read_product import get_product_by_id

def add_product(name: str, sku: str, price: float):
    """Insert product with items in MySQL"""
    if not name or not sku or not price or float(price) <= 0:
        raise ValueError("Vous devez indiquer un nom, numéro SKU et prix unitaire pour l'article.")
    
    session = get_sqlalchemy_session()

    try: 
        new_product = Product(name=name, sku=sku, price=price)
        session.add(new_product)
        session.flush() 
        session.commit()
        return new_product.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def add_product_sales_to_redis(sale_items: list):
    r = get_redis_conn()
    for item in sale_items:
        product_id = item['product_id']
        r.incr(f"product:{product_id}-{get_product_by_id(product_id)['name']}:sales", item['quantity'])

def delete_product_by_id(product_id: int):
    """Delete product by ID in MySQL"""
    session = get_sqlalchemy_session()
    try:
        product = session.query(Product).filter(Product.id == product_id).first()
        
        if product:
            session.delete(product)
            session.commit()
            return 1  
        else:
            return 0  
            
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

