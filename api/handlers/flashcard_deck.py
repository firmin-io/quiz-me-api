import json
import logging

from api.common import errors
from api.common.validation import validate_authorization_header_is_present, validate_user_exists_by_id
from api.data_access import flashcard_deck_dao
from api.model.model import FlashcardDeckModel
from api.utils import auth_utils
from api.utils.api_utils import build_response_with_body, build_response_without_body


def create_flashcard_deck(event, context):
    try:
        token = validate_authorization_header_is_present(event['headers'])
        auth_utils.decode_auth_token(token)
        deck_request = FlashcardDeckModel.from_request(json.loads(event['body']))
        validate_user_exists_by_id(deck_request.user_id)
        print('deck: ', deck_request.to_dynamo_dict())
        return build_response_with_body(201, flashcard_deck_dao.create(deck_request).to_dict())

    except errors.ApiError as ae:
        return errors.build_response_from_api_error(ae)

    except Exception as e:
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))


def update_flashcard_deck(event, context):
    try:
        token = validate_authorization_header_is_present(event['headers'])
        auth_utils.decode_auth_token(token)
        flashcard_deck_request = FlashcardDeckModel.from_update_request(json.loads(event['body']))
        logging.debug("flashcard deck request")
        logging.debug(flashcard_deck_request.description)
        flashcard_deck = flashcard_deck_dao.update(flashcard_deck_request)

        logging.debug(flashcard_deck)
        logging.debug(flashcard_deck.to_dict())

        return build_response_with_body(200, flashcard_deck.to_dict())

    except errors.ApiError as ae:
        return errors.build_response_from_api_error(ae)

    except Exception as e:
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))


def delete_flashcard_deck(event, context):
    try:
        token = validate_authorization_header_is_present(event['headers'])
        auth_utils.decode_auth_token(token)
        flashcard_deck_dao.delete(event['pathParameters']['flashcard_deck_id'])
        return build_response_without_body(204)

    except errors.ApiError as ae:
        return errors.build_response_from_api_error(ae)

    except KeyError as e:
        return errors.build_response_from_api_error(errors.Error('MISSING_REQUIRED_PARAMETER', str(e), 400))

    except Exception as e:
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))


def get_by_user_id(event, context):
    try:
        token = validate_authorization_header_is_present(event['headers'])
        auth_utils.decode_auth_token(token)

        items = flashcard_deck_dao.get_by_user_id(event['pathParameters']['user_id'])

        return build_response_with_body(200, [item.to_dict() for item in items if items])

    except errors.ApiError as ae:
        return errors.build_response_from_api_error(ae)

    except Exception as e:
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))


def get_flashcard_decks(event, context):
    try:
        items = flashcard_deck_dao.get_all()
        flashcard_decks = [item.to_dict() for item in items if items]
        return build_response_with_body(200, flashcard_decks)

    except errors.ApiError as ae:
        return errors.build_response_from_api_error(ae)

    except Exception as e:
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))


def get_by_flashcard_deck_id(event, context):
    try:
        token = validate_authorization_header_is_present(event['headers'])
        auth_utils.decode_auth_token(token)

        flashcard_deck = flashcard_deck_dao.get_by_id(event['pathParameters']['flashcard_deck_id'])

        return build_response_with_body(200, flashcard_deck.to_dict())

    except errors.ApiError as ae:
        return errors.build_response_from_api_error(ae)

    except Exception as e:
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))



