from pyscripts.database import CursorFromConnectionFromPool
from pyscripts.refactor import encrypt_password


class User:
    def __init__(self, name, password, account_type, user_code, _id):
        self.name = name
        self.password = password
        self.account_type = account_type
        self.user_code = user_code
        self._id = _id

    def __repr__(self):
        return f"<User {self.name}>"

    @classmethod
    def save_to_db_new_user(cls, name, password, account_type, user_code):
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

    @classmethod
    def login_user(cls, user_code, password):
        """This module logs the user into the system."""
        user = User.load_from_db_by_user_code(user_code)
        if user:
            secure_password = encrypt_password(password)
            if user.password == secure_password:
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def create_new_user(cls, user_code, user_name):
        if User.usercode_exists(user_code):
            return f"User {user_name} with user code {user_code} was not created as the user code already exist."
        else:
            User.save_to_db_new_user(user_name, encrypt_password("1234"), "user", user_code)
            return f"User {user_name} with user code {user_code} was created with password 1234!"

    @classmethod
    def usercode_exists(cls, user_code):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT _id FROM users WHERE user_code=%s',
                           (user_code,))
            user_check = cursor.fetchone()
            if user_check:
                return True
