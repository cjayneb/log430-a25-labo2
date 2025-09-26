"""
Orders (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from collections import defaultdict
from db import get_sqlalchemy_session, get_redis_conn
from sqlalchemy import desc
from models.order import Order

def get_order_by_id(order_id):
    """Get order by ID from Redis"""
    r = get_redis_conn()
    return r.hgetall(order_id)

def get_orders_from_mysql(limit=9999):
    """Get last X orders"""
    session = get_sqlalchemy_session()
    return session.query(Order).order_by(desc(Order.id)).limit(limit).all()

def get_orders_from_redis(limit=9999):
    """Get last x orders decided by the limit parameter"""
    r = get_redis_conn()
    orders_in_redis = []
    for i, key in enumerate(r.scan_iter("order:*")):
        if i >= limit:
            break
        order_data = r.hgetall(key)
        print(order_data)
        order_obj = Order.from_redis(order_data)
        orders_in_redis.append(order_obj)
    return orders_in_redis

def get_highest_spending_users():
    """Get report of highest spending users"""
    orders = get_orders_from_redis()
    expenses_by_user = defaultdict(float)
    for order in orders:
        expenses_by_user[order.user_id] += order.total_amount
    highest_spending_users = sorted(expenses_by_user.items(), key=lambda item: item[1], reverse=True)
    return highest_spending_users

def get_best_selling_products_v1():
    """Get report of best selling products"""
    orders = get_orders_from_redis()
    sales_by_product = defaultdict(float)
    for order in orders:
        for item in order.order_items:
            sales_by_product[item.product_id] += item.quantity
    best_selling_products = sorted(sales_by_product.items(), key=lambda item: item[1], reverse=True)
    return best_selling_products