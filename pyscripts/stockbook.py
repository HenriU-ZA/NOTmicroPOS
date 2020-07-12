from pyscripts.database import CursorFromConnectionFromPool


def get_all_stock(active='y', service='n'):
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute('SELECT * FROM stock_items WHERE active=%s AND service_item=%s ORDER BY item_name ASC',
                       (active, service))
        stock = cursor.fetchall()
        if stock:
            stock_list = []
            for item in stock:
                stock_list.append({'id': item[0], 'item_name': item[1], 'item_cost': item[2], 'labour_charge': item[3],
                                   'retail_price': item[4], 'stock_category_id': item[5], 'stock_qty': item[6],
                                   'order_qty': item[7], 'supplier_id': item[8], 'pending_qty': item[11]})
            return stock_list


def get_one_stock_item(item_id):
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute('SELECT * FROM stock_items WHERE id=%s', (item_id,))
        item = cursor.fetchone()
        if item:
            return [{'id': item[0], 'item_name': item[1], 'item_cost': item[2], 'labour_charge': item[3],
                     'retail_price': item[4], 'stock_category_id': item[5], 'stock_qty': item[6],
                     'order_qty': item[7], 'supplier_id': item[8], 'pending_qty': item[11]}]


def retrieve_supplier_names():
    """Returns all suppliers."""
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute('SELECT * FROM suppliers')
        suppliers = cursor.fetchall()
        if suppliers:
            better_suppliers = []
            for supplier in suppliers:
                better_suppliers.append({'id': supplier[0], 'name': supplier[1]})
            return better_suppliers


def retrieve_category_names():
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute('SELECT * FROM stock_category')
        categories = cursor.fetchall()
        if categories:
            category_list = []
            for category in categories:
                category_list.append({'category_id': category[0], 'category_name': category[1]})
            return category_list


def toggle_item(active, item_id):
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute('UPDATE stock_items SET active=%s WHERE id=%s', (active, item_id))


def update_item(data):
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute('UPDATE stock_items SET item_name=%s, labour_charge=%s, retail_price=%s WHERE id=%s',
                       (data['item_name'], data['labour_charge'], data['rrp'], data['item_id']))
