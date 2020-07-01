from pyscripts.user import User
from pyscripts.suppliers import Supplier
from pyscripts.refactor import encrypt_password
from pyscripts.details import Details
from pyscripts.confirm import confirm_passwords
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


def dashboard_page_formats(data):
    if data['todo'] == 'change_password':
        return [data['todo'], None,
                'You can update your password by entering you current password, and your new password.',
                'Change my password']
    elif data['todo'] == 'changing_password':
        message = None
        check = confirm_passwords(data['current_password'], data['new_password'], data['confirm_password'])
        if check[0]:
            if User.reset_user('password', encrypt_password(data['new_password']), g.user._id):
                message = 'Password Change was successful!'
        else:
            message = check[1]

        return [data['todo'], message,
                'I have changed my password.',
                'Changed my password']


def suppliers_page_formats(data):
    if data['todo'] == 'new_supplier':
        return [data['todo'], 'Create new supplier', 'Please fill the details of the new supplier']
    elif data['todo'] == 'create_supplier':
        Supplier.save_to_db_new_supplier(data['name'], data['contact_person'], data['contact_number'],
                                         data['contact_email'], data['address'], data['website'])
        result = 'Supplier created!'
        return [data['todo'], 'Created new supplier', 'You have attempted to create a new supplier', result]
    elif data['todo'] == 'view_suppliers':
        return [data['todo'], 'View Suppliers', 'A list of all registered suppliers', Supplier.view_all_suppliers()]
    elif data['todo'] == 'update':
        return [data['todo'], 'Update Supplier', 'Update the supplier details below',
                Supplier.load_details_from_db(data['supplier'])]
    elif data['todo'] == 'updating_supplier':
        message = "a"
        if Supplier.update_details(data):
            message = "Update Successful!"
        return [data['todo'], 'Updating Supplier', 'Supplier details is being updated', message]
        # return [data['todo'], data['cc'], data, message]
