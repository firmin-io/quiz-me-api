from passlib.hash import pbkdf2_sha256
from api.common import errors


def hash_password(password):
    try:
        return pbkdf2_sha256.hash(password)

    except Exception as e:
        raise errors.ApiError(errors.internal_server_error, e)


def check_password(password, password_hash):
    try:
        if not pbkdf2_sha256.verify(password, password_hash):
            raise errors.ApiError(errors.invalid_user_name_or_password)

    except Exception as e:
        print('unable to check password')
        raise errors.ApiError(errors.failed_to_login, e)
