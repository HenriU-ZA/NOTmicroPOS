from database import CursorFromConnectionFromPool


class User:
    def __init__(self, name, password, account_type, user_code, _id):
        self.name = name
        self.password = password
        self.account_type = account_type
        self.user_code = user_code
        self._id = _id

    def __repr__(self):
        return f"<User {self.name}>"

    def save_to_db_new_user(self, name, password, account_type, user_code):
        """This module will save a new user to the database"""
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute(
                'INSERT INTO users(name, password, account_type, user_code) '
                'VALUES(%s, %s, %s, %s)',
                (name, password, account_type, user_code))

    @classmethod
    def load_from_db_by_user_code(cls, user_code):
        """This module loads a user from the database, using the user code."""
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM users WHERE user_code=%s',
                           (user_code,))
            user_data = cursor.fetchone()
            if user_data:
                return cls(name=user_data[1],
                           password=user_data[2],
                           account_type=user_data[3],
                           user_code=user_data[4],
                           _id=user_data[0])

