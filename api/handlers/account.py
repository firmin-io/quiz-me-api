import json

from api.common import errors, validation
from api.model.model import LoginRequestModel, UserModel
from api.data_access import user_dao as ud
from api.utils import hash_utils, auth_utils
from api.utils.api_utils import build_response_with_body


def login(event, context):
    try:
        login_request = LoginRequestModel.from_request_json(event['body'])
        user = ud.get_by_email(login_request.email)
        # this throws an exception if the passwords don't match
        hash_utils.check_password(login_request.password, user.password)
        return build_response_with_body(200, {'id': user.id,
                                              'first_name': user.first_name,
                                              'last_name': user.last_name,
                                              'email': user.email,
                                              'token': auth_utils.generate_auth_token(user.id).decode()})

    except errors.ApiError as ae:
        return errors.build_response_from_api_error(ae)

    except Exception as e:
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))


def register(event, context):
    try:
        print('register')
        user_request = UserModel.from_request_json(event['body'])
        print('user model:')
        print(user_request)
        validation.validate_email(user_request.email)
        validate_user_does_not_exist(user_request.email)
        print('user does not exist, proceeding with creation')
        user = ud.create(user_request)
        res = build_response_with_body(200, {'id': user.id,
                                             'first_name': user.first_name,
                                             'last_name': user.last_name,
                                             'email': user.email,
                                             'token': auth_utils.generate_auth_token(
                                                 user.id).decode()})
        return res

    except errors.ApiError as ae:
        return errors.build_response_from_api_error(ae)

    except Exception as e:
        print(e)
        print(str(e))
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))


def validate_user_does_not_exist(email):
    try:
        user = ud.get_by_email(email)
        print('user.id {}'.format(user.id))
        raise errors.ApiError(errors.already_registered)
    except errors.ApiError as e:
        print(e)
        if e.api_error.issue == 'ALREADY_REGISTERED':
            print('user exists')
            raise e

    except Exception as e:
        if e == 'list index out of range':
            return
