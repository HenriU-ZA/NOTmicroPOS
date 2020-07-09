from pyscripts.user import User
import pyscripts.stock_setup as stock_setup
import pyscripts.stockbook as stockbook
from pyscripts.suppliers import Supplier
import pyscripts.refactor as refactor
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
        if User.reset_user('password', refactor.encrypt_password("1234"), todo['user']):
            message = "Password reset has been successful."
        return [message, todo['todo']]
    elif todo['todo'] == 'update_details':
        return [None, todo['todo']]
    elif todo['todo'] == 'updating':
        Details.update_details(g.details, todo)
        Details.save_details_do_db(g.details)
        return ['Details has been updated!', todo['todo']]
    elif todo['todo'] == 'disabled_cats':
        return [todo['todo'], 'View Stock Categories', 'See all stock categories', stock_setup.load_all_categories("n")]
    elif todo['todo'] == 'enable_cat':
        return [todo['todo'], 'Re-Enabled Category', 'This category has been reinstated',
                stock_setup.toggle_enabled(todo, 'y')]
    elif todo['todo'] == 'rename_cat':
        return [todo['todo'], 'Rename Category', 'This category will be renamed',
                stock_setup.load_one_category(todo['cat_id'])]
    elif todo['todo'] == 'rename_cat_go':
        stock_setup.rename_category(todo)
        message = "Renamed Successfully."
        return [todo['todo'], 'Rename Category', message]
    elif todo['todo'] == 'disabled_supps':
        return [todo['todo'], 'View Disabled Suppliers', 'See all disabled Suppliers', Supplier.view_all_suppliers("n")]
    elif todo['todo'] == 'enable_supp':
        return [todo['todo'], 'Re-Enabled Supplier', 'This supplier has been reinstated',
                Supplier.toggle_suppliers(todo['supp_id'], 'y')]

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
            if User.reset_user('password', refactor.encrypt_password(data['new_password']), g.user._id):
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
    elif data['todo'] == 'disable_supp':
        return [data['todo'], 'Removed Supplier', 'This supplier has been removed',
                Supplier.toggle_suppliers(data['disable_id'], 'n')]


def stock_setup_page_formats(data):
    if data['todo'] == 'new_category':
        return [data['todo'], 'Create new stock category', 'Enter name for the new stock category']
    elif data['todo'] == 'creating_category':
        if stock_setup.create_category(data):
            message = 'Success!'
        else:
            message = 'Fail!'
        return [data['todo'], 'Creating new stock category', 'Trying to create a new stock category', message]
    elif data['todo'] == 'view_categories':
        return [data['todo'], 'View Stock Categories', 'See all stock categories', stock_setup.load_all_categories()]
    elif data['todo'] == 'disable':
        return [data['todo'], 'Removed Category', 'This category has been removed', stock_setup.toggle_enabled(data, 'n')]
    elif data['todo'] == 'new_stock_item':
        return [data['todo'], Supplier.view_all_suppliers(), stock_setup.load_all_categories()]
    elif data['todo'] == 'stock_create':
        return [data['todo'], 'Created Stock Item', 'Item has been created', stock_setup.create_stock_item(data)]


def view_stock_page_formats(data):
    stock = None
    # if data['todo'] == 'view_stock' and data['what'] == 'all':
    #     stock = refactor.ammend_stock(stockbook.get_all_stock(), stockbook.retrieve_supplier_names(), stockbook.retrieve_category_names())
    #
    # elif data['todo'] == 'view_stock' and data['what'] == 'service':
    #     stock = refactor.ammend_stock(stockbook.get_all_stock('y', 'y'), stockbook.retrieve_supplier_names(), stockbook.retrieve_category_names())

    if data['todo'] == 'view_stock' and data['what'] == 'search':
        stockq = refactor.ammend_stock(stockbook.get_all_stock('y', data['s_i']), stockbook.retrieve_supplier_names(), stockbook.retrieve_category_names())
        stock = refactor.stock_search(stockq, data['term'])

    return [data['todo'], stock, refactor.count_cost(stock), data['cols']]

