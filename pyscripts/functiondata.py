from pyscripts.database import CursorFromConnectionFromPool

class FunctionData:
    def __init__(self, name, description, used, title, _id):
        self.name = name
        self.description = description
        self.used = used
        self.title = title
        self._id = _id

    def __repr__(self):
        return f"<Function {self.name}>"

    # def save_to_db_new_user(self, name, password, account_type, user_code):
    #     """This module will save a new user to the database"""
    #     with CursorFromConnectionFromPool() as cursor:
    #         cursor.execute(
    #             'INSERT INTO users(name, password, account_type, user_code) '
    #             'VALUES(%s, %s, %s, %s)',
    #             (name, password, account_type, user_code))

    @classmethod
    def load_from_db_by_name(cls, name):
        """This module loads a user from the database, using the user code."""
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM functiondata WHERE func_name=%s',
                           (name,))
            function_data = cursor.fetchone()
            if function_data:
                return cls(name=function_data[1],
                           description=function_data[2],
                           used=function_data[3],
                           title=function_data[4],
                           _id=function_data[0])

    @classmethod
    def format_page_data(cls, name, username, optional_message=""):
        title = "Unknown"
        username = username
        optional_message = optional_message
        data = FunctionData.load_from_db_by_name(name)
        if data:
            title = data.title
        return {'title': title,
                'username': username,
                'optional_message': optional_message,
                'description': data.description}


