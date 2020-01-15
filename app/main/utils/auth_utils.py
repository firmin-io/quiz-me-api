import datetime

import jwt

from app.main.common import errors

__key = '31c90408-eb0f-4120-b125-c88c1491cb6e-quiz-me-2020'


def generate_auth_token(user_id):
    """
            Generates the Auth Token
            :return: string
            """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        token = jwt.encode(
            payload,
            __key,
            algorithm='HS256'
        )
        return token
    except Exception as e:
        print(str(e))
        raise errors.ApiError(errors.internal_server_error)


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, __key)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise errors.ApiError(errors.unauthorized)
    except jwt.InvalidTokenError:
        raise errors.ApiError(errors.unauthorized)