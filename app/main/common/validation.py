import re

from app.main.common import errors
from app.main.data_access import user_dao


def validate_item_exists(response):
    try:
        return response['Item']
    except KeyError:
        raise errors.ApiError(errors.not_found)


def validate_items_exist(response, quietly=False):
    try:
        return response['Items']
    except KeyError as e:
        print(str(e))
        if quietly:
            return []
        raise errors.ApiError(errors.not_found)


def validate_items_exist_quietly(response):
    return validate_items_exist(response, True)


def validate_user_exists(email):
    try:
        user = user_dao.get_by_email(email)
        print('user.id {}'.format(user.id))
    except errors.ApiError as e:
        if e.api_error.issue == 'NOT_FOUND':
            raise errors.ApiError(errors.invalid_user_id)
        return


def validate_request_id_header_is_present(request):
    try:
        request_id = str(request.headers['Request-Id'])
        if len(request_id) < 1:
            raise errors.ApiError(errors.invalid_request_id)
        return request_id
    except KeyError:
        raise errors.ApiError(errors.invalid_request_id)


def validate_authorization_header_is_present(request):
    try:
        token = str(request.headers['Authorization'])
        if len(token) < 1:
            raise errors.ApiError(errors.invalid_auth_token)
        return token
    except KeyError:
        raise errors.ApiError(errors.invalid_auth_token)


def validate_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,5})+$'
    if re.search(regex, email):
        return

    raise errors.ApiError(errors.invalid_email)




