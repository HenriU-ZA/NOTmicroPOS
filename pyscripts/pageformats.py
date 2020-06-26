from pyscripts.user import User
from pyscripts.refactor import encrypt_password
from pyscripts.details import Details
from flask import g


def superuser_page_formats(todo):
    if todo['todo'] == 'view_users':
        users = User.view_all_users()
        return [users, todo['todo']]
    elif todo['todo'] == 'add_user':
        return [None, todo['todo']]
    elif todo['todo'] == 'creating':
        return [User.create_new_user(todo['user_code'], todo['user_name']), todo['todo']]
    elif todo['todo'] == 'rename':
        return [User.load_from_db_by_user_code(todo['user']), todo['todo']]
    elif todo['todo'] == 'renaming':
        if User.reset_user('name', todo['user_rename'], todo['user']):
            return ['Name change successful.', todo['todo']]
    elif todo['todo'] == 'reset':
        message = "Something went wrong. Password was not reset."
        if User.reset_user('password', encrypt_password("1234"), todo['user']):
            message = "Password reset has been successful."
        return [message, todo['todo']]
    elif todo['todo'] == 'update_details':
        return [None, todo['todo']]
    elif todo['todo'] == 'updating':
        Details.update_details(g.details, todo)
        Details.save_details_do_db(g.details)
        return ['Details has been updated!', todo['todo']]
    else:
        return [None, None]