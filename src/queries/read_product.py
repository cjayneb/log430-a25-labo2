"""
Product (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from sqlalchemy import desc
from db import get_redis_conn, get_sqlalchemy_session
from models.product import Product

def get_product_by_id(product_id):
    """Get product by ID """
    session = get_sqlalchemy_session()
    result = session.query(Product).filter_by(id=product_id).all()

    if len(result):
        return {
            'id': result[0].id,
            'name': result[0].name,
            'sku': result[0].sku,
            'price': result[0].price
        }
    else:
        return {}

def get_products(limit=9999):
    """Get last X products"""
    session = get_sqlalchemy_session()
    return session.query(Product).order_by(desc(Product.id)).limit(limit).all()

def get_products_sales_from_redis():
    """Get last x products decided by the limit parameter"""
    r = get_redis_conn()
    sales_data = {}
    for key in r.scan_iter(match="product:*:sales"):
        product = key.split(":")[1]
        sales_data[product] = int(r.get(key))
    return sales_data

def get_best_selling_products_v2():
    """Get report of best selling products"""
    products = get_products_sales_from_redis()
    print(products)
    return sorted(products.items(), key=lambda item: item[1], reverse=True)
