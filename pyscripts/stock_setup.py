from pyscripts.database import CursorFromConnectionFromPool


def create_category(data):
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute(
            'INSERT INTO stock_category(category) VALUES(%s)', (data['category_name'], ))
        return True
