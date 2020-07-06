from pyscripts.database import CursorFromConnectionFromPool


def create_category(data):
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute(
            'INSERT INTO stock_category(category, enable) VALUES(%s, %s)', (data['category_name'], "y"))
        return True


def create_stock_item(data):
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute(
            'INSERT INTO stock_items(item_name, item_cost, labour_charge, retail_price, stock_category_id, stock_qty, '
            'order_qty, supplier_id, service_item) '
            'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)', (
             data['item_name'], data['item_cost'], data['labour_charge'], data['retail_price'], data['stock_category'],
             0, 0, data['supplier'], data['service']))
        return True


def load_all_categories(enable='y'):
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute('SELECT * FROM stock_category WHERE enable=%s ', (enable,))
        categories = cursor.fetchall()
        if categories:
            category_list = []
            for category in categories:
                category_list.append({'category_id': category[0], 'category_name': category[1]})
            return category_list


def load_one_category(c_id):
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute('SELECT * FROM stock_category WHERE id=%s', (c_id,))
        one_cat = cursor.fetchone()
        if one_cat:
            return {'category_id': one_cat[0], 'category_name': one_cat[1]}


def toggle_enabled(data, enable):
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute('UPDATE stock_category SET enable=%s WHERE id=%s', (enable, data['cat_id']))


def rename_category(data):
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute('UPDATE stock_category SET category=%s WHERE id=%s', (data['new_name'], data['cat_id']))
