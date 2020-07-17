from pyscripts.database import CursorFromConnectionFromPool
from datetime import datetime


def add_item_to_order(item, qty):
    if not check_for_open_order(item[0]['supplier_id']):
        create_new_order(item[0]['supplier_id'])
    order_id = get_order_id(item[0]['supplier_id'])[0]
    add_item_now(item, qty, order_id)
    return {'order_id': order_id, 'supplier_name': item[0]['supplier_name']}


def add_item_now(item, qty, order_id):
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute(
            'INSERT INTO order_items(order_id, order_qty, received_qty, unit_cost, item_id) VALUES(%s, %s, %s, %s, %s)',
            (order_id, qty, 0, item[0]['item_cost'], item[0]['id']))
        return True


def build_order_items(order_id):
    item_list=[]
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute('SELECT * FROM order_items WHERE order_id=%s', (order_id,))
        order_items = cursor.fetchall()
        if order_items:
            for item in order_items:
                item_list.append({'qty': item[2], 'est_cost': item[2]*item[4], 'unit_cost': item[4], 'name': item[5]})
    return item_list


def check_for_open_order(supplier_id):
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute('SELECT * FROM purchase_orders WHERE supplier_id=%s AND order_status=%s ', (supplier_id, 'open'))
        order_open = cursor.fetchone()
        if order_open:
            return True


def create_new_order(supplier_id):
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute(
            'INSERT INTO purchase_orders(supplier_id, order_date, order_status) VALUES(%s, %s, %s)',
            (supplier_id, datetime.now(), "open"))
        return True


def get_order_id(supplier_id):
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute('SELECT order_id FROM purchase_orders WHERE supplier_id=%s AND order_status=%s ',
                       (supplier_id, 'open'))
        order_id = cursor.fetchone()
        if order_id:
            return order_id
