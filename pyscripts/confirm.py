from flask import g
from pyscripts.refactor import encrypt_password


def confirm_passwords(current, new, confirm):
    if encrypt_password(current) == g.user.password:
        if new == confirm:
            return [True, 'All Good, changing password.']
        else:
            return [False, 'Your password confirmation does not match your new password!']
    else:
        return [False, 'Your current password is incorrect!']
