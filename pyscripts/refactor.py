import hashlib


def encrypt_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def ammend_stock(stock, suppliers, categories):
    for item in stock:
        for supplier in suppliers:
            if item['supplier_id'] == supplier['id']:
                item['supplier_name'] = supplier['name']
        for category in categories:
            if item['stock_category_id'] == category['category_id']:
                item['category_name'] = category['category_name']
        item['total_cost'] = item['stock_qty'] * item['item_cost']
    return stock


def count_cost(stock):
    total_cost = 0
    total_qty = 0
    total_pend = 0
    total_orders = 0
    for item in stock:
        total_cost += item['total_cost']
        total_qty += item['stock_qty']
        total_pend += item['pending_qty']
        total_orders += item['order_qty']
    return {'total_cost': total_cost, 'total_qty': total_qty, 'total_pend': total_pend, 'total_orders': total_orders}


def stock_search(stock, term):
    stocklist = []
    for item in stock:
        if term.lower() in item['item_name'].lower() or term.lower() in item['supplier_name'].lower() or term.lower() in \
                item['category_name'].lower():
            stocklist.append(item)
    return stocklist
