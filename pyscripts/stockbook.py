from pyscripts.database import CursorFromConnectionFromPool


def get_all_stock(active='y', service='n'):
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute('SELECT * FROM stock_items WHERE active=%s AND service_item=%s ORDER BY item_name ASC', (active, service))
        stock = cursor.fetchall()
        if stock:
            stock_list = []
            for item in stock:
                stock_list.append({'id': item[0], 'item_name': item[1], 'item_cost': item[2], 'labour_charge': item[3],
                                   'retail_price': item[4], 'stock_category_id': item[5], 'stock_qty': item[6],
                                   'order_qty': item[7], 'supplier_id': item[8]})
            return stock_list
