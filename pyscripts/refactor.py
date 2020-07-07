import hashlib


def encrypt_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def ammend_stock(stock):
    for item in stock:
        item['supplier_name'] = 'sup_name'
        item['category_name'] = 'cat_name'
        item['total_cost'] = item['stock_qty'] * item['item_cost']
    return stock

def count_cost(stock):
    total_cost = 0
    for item in stock:
        total_cost += item['total_cost']
    return total_cost
