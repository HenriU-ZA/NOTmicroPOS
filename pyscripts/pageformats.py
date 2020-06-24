from pyscripts.user import User


def superuser_page_formats(todo):
    if todo == 'view_users':
        users = User.view_all_users()
        return [users, todo]
    elif:
        # NEED TO ADD THE ADDUSER OPTION TO THIS PAGE AND REMOVE ADDITIONAL HTML TEMPLATE
