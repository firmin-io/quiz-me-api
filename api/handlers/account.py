import json
import logging

from api.common import errors, validation
from api.data_access import user_dao as ud
from api.model.model import LoginRequestModel, UserModel
from api.utils import auth_utils, hash_utils
from api.utils.api_utils import build_response_with_body


def login(event, context):
    try:
        login_request = LoginRequestModel.from_request(json.loads(event['body']))
        user = ud.get_by_email(login_request.email)
        # this throws an exception if the passwords don't match
        hash_utils.check_password(login_request.password, user.password)
        return build_response_with_body(200, {'id': user.id,
                                              'first_name': user.first_name,
                                              'last_name': user.last_name,
                                              'email': user.email,
                                              'token': auth_utils.generate_auth_token(user.id).decode()})

    except errors.ApiError as e:
        print('boo')
        print(e)
        if e.api_error.issue == 'NOT_FOUND':
            print("wtffff")
            return errors.build_response_from_api_error(errors.ApiError(errors.invalid_user_name_or_password))
        else:
            return errors.build_response_from_api_error(e)

    except Exception as e:
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))


def register(event, context):
    try:
        logging.debug('register')
        user_request = UserModel.from_request(json.loads(event['body']))
        logging.debug('user model:')
        logging.debug(user_request)
        validation.validate_email(user_request.email)
        validate_user_does_not_exist(user_request.email)
        logging.debug('user does not exist, proceeding with creation')
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
        logging.debug(e)
        logging.debug(str(e))
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))


def validate_user_does_not_exist(email):
    try:
        user = ud.get_by_email(email)
        logging.debug('user.id {}'.format(user.id))
        raise errors.ApiError(errors.already_registered)
    except errors.ApiError as e:
        logging.debug(e)
        if e.api_error.issue == 'ALREADY_REGISTERED':
            logging.debug('user exists')
            raise e

    except Exception as e:
        if e == 'list index out of range':
            return
