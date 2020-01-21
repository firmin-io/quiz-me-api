from flask import request
from flask_restful import Resource

from app.main.common import errors, validation
from app.main.data_access import user_dao as dao
from app.main.model.model import UserModel
from app.main.utils import auth_utils, id_utils, logging_utils


class RegisterResource(Resource):

    def post(self):
        logger = logging_utils.ApiLogger(id_utils.generate_debug_id())
        try:
            user_request = UserModel.from_request_json(request.json)
            validation.validate_email(user_request.email)
            validate_user_does_not_exist(user_request.email)
            user = dao.create(user_request)
            return {'id': user.id,
                    'first_name': user.first_name,
                    'email': user.email,
                    'token': auth_utils.generate_auth_token(user.id).decode()}, 200

        except errors.ApiError as ae:
            return errors.build_response_from_api_error(ae)

        except Exception as e:
            return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e), logger)

    def get(self):
        return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))

    def put(self):
        return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))

    def delete(self):
        return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))


def validate_user_does_not_exist(email):
    try:
        user = dao.get_by_email(email)
        print('user.id {}'.format(user.id))
        raise errors.ApiError(errors.already_registered)
    except errors.ApiError as e:
        if e.api_error.issue == 'ALREADY_REGISTERED':
            raise e

