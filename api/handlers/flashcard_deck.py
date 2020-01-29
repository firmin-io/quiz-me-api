import json

from api.common import errors
from api.common.validation import validate_authorization_header_is_present, validate_user_exists_by_id
from api.data_access import flashcard_deck_dao
from api.model.model import FlashcardDeckModel
from api.utils import auth_utils
from api.utils.api_utils import build_response_with_body


def create_flashcard_deck(event, context):
    try:
        token = validate_authorization_header_is_present(event['headers'])
        auth_utils.decode_auth_token(token)
        deck_request = FlashcardDeckModel.from_request_json(json.loads(event['body']))
        validate_user_exists_by_id(deck_request.user_id)
        print('deck: ', deck_request.to_dynamo_dict())
        return build_response_with_body(201, flashcard_deck_dao.create(deck_request).to_dict())

    except errors.ApiError as ae:
        return errors.build_response_from_api_error(ae)

    except Exception as e:
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))


def put(self):
    return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))


def delete(self):
    return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))


def get_by_user_id(event, context):
    try:
        token = validate_authorization_header_is_present(event['headers'])
        auth_utils.decode_auth_token(token)

        items = flashcard_deck_dao.get_by_user_id(event['pathParameters']['user_id'])

        json = [item.to_dict() for item in items if items]

        return build_response_with_body(200, json)

    except errors.ApiError as ae:
        return errors.build_response_from_api_error(ae)

    except Exception as e:
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))



