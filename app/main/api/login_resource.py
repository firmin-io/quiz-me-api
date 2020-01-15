from flask import request
from flask_restful import Resource

from app.main.common import errors
from app.main.data_access import user_dao as ud
from app.main.model.model import LoginRequestModel
from app.main.utils import auth_utils, hash_utils, logging_utils, id_utils


class LoginResource(Resource):

    def post(self):
        logger = logging_utils.ApiLogger(id_utils.generate_debug_id())
        try:
            login_request = LoginRequestModel.from_request_json(request.json)
            user = ud.get_by_email(login_request.email)
            # this throws an exception is the passwords don't match
            hash_utils.check_password(login_request.password, user.password)
            return {'id': user.id, 'token': auth_utils.generate_auth_token(user.id).decode()}, 200

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
