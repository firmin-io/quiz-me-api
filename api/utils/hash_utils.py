from api.pybcrypt import bcrypt
from api.common import errors


def hash_password(password):
    try:
        return bcrypt.hashpw(password, bcrypt.gensalt(10))
    except Exception as e:
        print('unable to create hash')
        print(e)
        raise errors.ApiError(errors.internal_server_error, e)


def check_password(password, password_hash):
    try:
        return bcrypt.hashpw(password, password_hash) == password_hash
    except Exception as e:
        print('unable to check password')
        raise errors.ApiError(errors.failed_to_login, e)
