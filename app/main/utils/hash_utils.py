import bcrypt
from app.main.common import errors


def hash_password(password):
    try:
        return bcrypt.hashpw(password, bcrypt.gensalt(2))
    except Exception:
        raise errors.ApiError(errors.internal_server_error)


def check_password(password, password_hash):
    try:
        return bcrypt.checkpw(password, password_hash)
    except Exception:
        raise errors.ApiError(errors.failed_to_login)
