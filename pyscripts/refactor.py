import hashlib


def encrypt_password(password):
    return hashlib.md5(password.encode()).hexdigest()
