from flask import request
from flask_restful import Resource

from api.common import errors
from api.common.validation import validate_authorization_header_is_present, validate_user_exists
from api.data_access import flashcard_deck_dao
from api.model.model import FlashcardDeckModel
from api.utils import auth_utils


class FlashcardDecksResource(Resource):

    def post(self):
        try:
            token = validate_authorization_header_is_present(request)
            auth_utils.decode_auth_token(token)
            deck_request = FlashcardDeckModel.from_request_json(request.json)
            validate_user_exists(deck_request.user_id)
            return flashcard_deck_dao.create(deck_request).to_dict(), 201

        except errors.ApiError as ae:
            return errors.build_response_from_api_error(ae)

        except Exception as e:
            return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))

    def get(self):
        return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))

    def put(self):
        return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))

    def delete(self):
        return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))


class UserFlashcardDecksResource(Resource):

    def get(self, user_id):
        try:
            token = validate_authorization_header_is_present(request)
            auth_utils.decode_auth_token(token)

            items = flashcard_deck_dao.get_by_user_id(user_id)

            json = [item.to_dict() for item in items if items]

            return json, 200

        except errors.ApiError as ae:
            return errors.build_response_from_api_error(ae)

        except Exception as e:
            return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))

    def post(self):
        return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))

    def put(self):
        return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))

    def delete(self):
        return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))
