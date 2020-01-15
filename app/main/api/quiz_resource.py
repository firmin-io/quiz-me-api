import re

from flask import request
from flask_restful import Resource

from app.main.common import errors
from app.main.common.validation import validate_authorization_header_is_present
from app.main.data_access import quiz_dao
from app.main.model.model import QuizModel
from app.main.utils import auth_utils, id_utils, logging_utils


class QuizzesResource(Resource):

    def post(self):
        logger = logging_utils.ApiLogger(id_utils.generate_debug_id())
        try:
            quiz_request = QuizModel.from_request_json(request.json)
            token = validate_authorization_header_is_present(request)
            auth_utils.decode_auth_token(token)
            return quiz_dao.create(quiz_request).to_json(), 201

        except errors.ApiError as ae:
            return errors.build_response_from_api_error(ae, logger)

        except Exception as e:
            return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e), logger)

    def get(self):
        return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))

    def put(self):
        return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))

    def delete(self):
        return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))


class UserQuizzesResource(Resource):

    def get(self, user_id):
        logger = logging_utils.ApiLogger(id_utils.generate_debug_id())
        try:
            token = validate_authorization_header_is_present(request)
            auth_utils.decode_auth_token(token)
            json = []
            items = quiz_dao.get_by_user_id(user_id, True)

            for item in items:
                json.append(item.to_json())

            return json, 200

        except errors.ApiError as ae:
            return errors.build_response_from_api_error(ae)

        except Exception as e:
            return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e), logger)

    def post(self):
        return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))

    def put(self):
        return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))

    def delete(self):
        return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))


