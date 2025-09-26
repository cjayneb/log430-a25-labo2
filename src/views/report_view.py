"""
Report view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from queries.read_order import get_best_selling_products_v1, get_highest_spending_users
from queries.read_user import get_user_by_id
from queries.read_product import get_best_selling_products_v2, get_product_by_id
from views.template_view import get_template

def show_highest_spending_users():
    """ Show report of highest spending users """
    spending_data = get_highest_spending_users()
    rows = []
    for user_id, total in spending_data:
        user = get_user_by_id(user_id)
        user_name = f"{user['id']} - {user['name']}"
        rows.append(f"<tr><td>{user_name}</td><td>${total:.2f}</td></tr>")

    return get_template(f"""
        <h2>Les plus gros acheteurs</h2>
        <table class="table">
            <tr>
                <th>Utilisateur</th>
                <th>Total dépensé</th>
            </tr>
            {"".join(rows)}
        </table>
    """)

def show_best_sellers_v1():
    """ Show report of best selling products """
    best_selling_products = get_best_selling_products_v1()
    rows = []
    for product_id, total_sold in best_selling_products:
        rows.append(f"<tr><td>{get_product_by_id(product_id)['name']}</td><td>{total_sold}</td></tr>")

    return get_template(f"""
        <h2>Les articles les plus vendus</h2>
        <table class="table">
            <tr>
                <th>Produit</th>
                <th>Total vendu(s)</th>
            </tr>
            {"".join(rows)}
        </table>
    """)

def show_best_sellers_v2():
    """ Show report of best selling products """
    best_selling_products = get_best_selling_products_v2()
    rows = []
    for product_name, total_sold in best_selling_products:
        rows.append(f"<tr><td>{product_name}</td><td>{total_sold}</td></tr>")

    return get_template(f"""
        <h2>Les articles les plus vendus</h2>
        <table class="table">
            <tr>
                <th>Produit</th>
                <th>Total vendu(s)</th>
            </tr>
            {"".join(rows)}
        </table>
    """)