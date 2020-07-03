from pyscripts.database import CursorFromConnectionFromPool


def create_category(data):
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute(
            'INSERT INTO stock_category(category, enable) VALUES(%s, %s)', (data['category_name'], "y"))
        return True


def load_all_categories(enable='y'):
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute('SELECT * FROM stock_category WHERE enable=%s ', (enable, ))
        categories = cursor.fetchall()
        if categories:
            category_list = []
            for category in categories:
                category_list.append({'category_id': category[0], 'category_name': category[1]})
            return category_list


def toggle_enabled(data, enable):
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute('UPDATE stock_category SET enable=%s WHERE id=%s', (enable, data['cat_id']))

