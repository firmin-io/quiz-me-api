from api.pybcrypt import bcrypt
from api.common import errors


def hash_password(password):
    try:
        return bcrypt.hashpw(password, bcrypt.gensalt(10))
    except Exception:
        raise errors.ApiError(errors.internal_server_error)


def check_password(password, password_hash):
    try:
        return bcrypt.hashpw(password, password_hash) == password_hash
    except Exception:
        raise errors.ApiError(errors.failed_to_login)
