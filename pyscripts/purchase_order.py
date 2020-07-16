from pyscripts.database import CursorFromConnectionFromPool
from datetime import datetime

def add_item_to_order(item, qty):
    if not check_for_open_order(item[0]['supplier_id']):
        create_new_order(item[0]['supplier_id'])
    # GET ORDER ID
    # ADD ITEM TO ORDER
    return 'done'


def check_for_open_order(supplier_id):
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute('SELECT * FROM purchase_orders WHERE supplier_id=%s AND order_status=%s ', (supplier_id, 'open'))
        order_open = cursor.fetchone()
        if order_open:
            return True

def create_new_order(supplier_id):
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute(
            'INSERT INTO purchase_orders(supplier_id, order_date, order_status) VALUES(%s, %s, %s)', (supplier_id, datetime.now(), "open"))
        return True
