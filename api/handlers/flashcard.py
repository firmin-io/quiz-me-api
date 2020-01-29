import json
import logging

from api.common import errors
from api.common.validation import validate_authorization_header_is_present, validate_user_exists_by_id
from api.data_access import flashcard_dao, flashcard_deck_dao
from api.model.model import FlashcardModel
from api.utils import auth_utils
from api.utils.api_utils import build_response_with_body, build_response_without_body


def create_flashcard(event, context):
    try:
        token = validate_authorization_header_is_present(event['headers'])
        auth_utils.decode_auth_token(token)
        flashcard_request = FlashcardModel.from_request_json(json.loads(event['body']))
        validate_flashcard_deck_exists(flashcard_request.flashcard_deck_id)
        return build_response_with_body(201, flashcard_dao.create(flashcard_request).to_dict())

    except errors.ApiError as ae:
        return errors.build_response_from_api_error(ae)

    except Exception as e:
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))


def update_flashcard(event, context):
    return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))


def delete_flashcard(event, context):
    try:
        token = validate_authorization_header_is_present(event['headers'])
        auth_utils.decode_auth_token(token)
        flashcard_dao.delete(event['pathParameters']['flashcard_id'])
        return build_response_without_body(204)

    except errors.ApiError as ae:
        return errors.build_response_from_api_error(ae)

    except KeyError as e:
        return errors.build_response_from_api_error(errors.Error('MISSING_REQUIRED_PARAMETER', str(e), 400))

    except Exception as e:
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))


def validate_flashcard_deck_exists(flashcard_deck_id):
    try:
        flashcard_deck = flashcard_deck_dao.get_by_id(flashcard_deck_id)
        logging.debug('deck id {}'.format(flashcard_deck.id))
        return
    except errors.ApiError as e:
        if e.api_error.issue == 'NOT_FOUND':
            raise errors.ApiError(errors.invalid_flashcard_deck_id)
        return
