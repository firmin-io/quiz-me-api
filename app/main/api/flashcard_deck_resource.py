import re

from flask import request
from flask_restful import Resource

from app.main.common import errors
from app.main.common.validation import validate_authorization_header_is_present, validate_user_exists
from app.main.data_access import flashcard_deck_dao
from app.main.model.model import FlashcardDeckModel
from app.main.utils import auth_utils, id_utils, logging_utils


class FlashcardDecksResource(Resource):

    def post(self):
        logger = logging_utils.ApiLogger(id_utils.generate_debug_id())
        try:
            token = validate_authorization_header_is_present(request)
            auth_utils.decode_auth_token(token)
            deck_request = FlashcardDeckModel.from_request_json(request.json)
            validate_user_exists(deck_request.user_id)
            return flashcard_deck_dao.create(deck_request).to_json(), 201

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


class UserFlashcardDecksResource(Resource):

    def get(self, user_id):
        logger = logging_utils.ApiLogger(id_utils.generate_debug_id())
        try:
            token = validate_authorization_header_is_present(request)
            auth_utils.decode_auth_token(token)

            items = flashcard_deck_dao.get_by_user_id(user_id)

            json = [item.to_json() for item in items if items]

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
