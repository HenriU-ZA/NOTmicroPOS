from pyscripts.user import User


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
    else:
        return [None, None]