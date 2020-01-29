from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from api.common import validation, errors
from api.data_access import dynamo_db as db
from api.model.model import FlashcardModel
from api.utils.id_utils import generate_id

table = db.dynamo_db.Table('qm_flashcard')


def get_by_flashcard_deck_id(flashcard_deck_id, quietly=False):
    try:
        response = table.query(
            IndexName="flashcard_deck_id-index",
            KeyConditionExpression=Key('flashcard_deck_id').eq(flashcard_deck_id)
        )
        items = validation.validate_items_exist(response, quietly)
        flashcards = [FlashcardModel.from_dynamo_json(item) for item in items if items]

        return flashcards

    except ClientError:
        raise errors.ApiError(errors.internal_server_error)

    except errors.ApiError as e:
        raise e

    except Exception as e:
        raise errors.ApiError(errors.internal_server_error)


def get_by_flashcard_deck_id_quietly(flashcard_deck_id):
    return get_by_flashcard_deck_id(flashcard_deck_id, True)


def get_by_id(_id):
    try:
        response = table.get_item(
            Key={
                'id': _id
            }
        )
        item = validation.validate_item_exists(response)
        return FlashcardModel.from_dynamo_json(item)

    except ClientError:
        raise errors.ApiError(errors.internal_server_error)

    except errors.ApiError as e:
        raise e

    except Exception:
        raise errors.ApiError(errors.internal_server_error)


def create(flashcard):
    try:
        _id = generate_id()
        flashcard.id = _id
        table.put_item(
            Item=flashcard.to_dynamo_dict()
        )
        return get_by_id(_id)

    except ClientError:
        raise errors.ApiError(errors.internal_server_error)

    except errors.ApiError as e:
        raise e

    except Exception:
        raise errors.ApiError(errors.internal_server_error)
