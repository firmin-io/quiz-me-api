from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from api.common import validation, errors
from api.data_access import dynamo_db as db, question_dao, flashcard_dao
from api.model.model import FlashcardDeckModel, QuizModel
from api.utils.id_utils import generate_id

table = db.dynamo_db.Table('qm_flashcard_deck')


def get_by_user_id(user_id):
    try:
        response = table.query(
            IndexName="user_id-index",
            KeyConditionExpression=Key('user_id').eq(user_id)
        )
        items = validation.validate_items_exist_quietly(response)
        decks = []
        for item in items:
            deck = FlashcardDeckModel.from_dynamo(item)
            flashcards = flashcard_dao.get_by_flashcard_deck_id_quietly(deck.id)
            deck.flashcards = flashcards
            decks.append(deck)

        return decks

    except ClientError:
        raise errors.ApiError(errors.internal_server_error)

    except errors.ApiError as e:
        raise e

    except Exception as e:
        errors.ApiError(errors.internal_server_error, e)



def delete(_id):
    try:
        flashcard_deck = get_by_id(_id)
        table.delete_item(
            Key={
                'id': _id
            }
        )

        print('deleted:', _id)
        for flashcard in flashcard_deck.flashcards:
            flashcard_dao.delete(flashcard.id)

    except errors.ApiError as e:
        if e.api_error.issue == 'NOT_FOUND':
            return

    except ClientError as e:
        raise errors.ApiError(errors.internal_server_error)

    except Exception as e:
        raise errors.ApiError(errors.internal_server_error, e)


def get_by_id(_id):
    try:
        print('getting deck by id')
        response = table.get_item(
            Key={
                'id': _id
            }
        )
        print('got deck by id')
        item = validation.validate_item_exists(response)
        print('got item')
        flashcard_deck = FlashcardDeckModel.from_dynamo(item)
        print(flashcard_deck)
        flashcards = flashcard_dao.get_by_flashcard_deck_id_quietly(_id)
        flashcard_deck.flashcards = flashcards
        return flashcard_deck

    except ClientError:
        raise errors.ApiError(errors.internal_server_error)

    except errors.ApiError as e:
        raise e

    except Exception as e:
        errors.ApiError(errors.internal_server_error, e)


def create(flashcard_deck):
    try:
        print('creating deck')

        _id = generate_id()
        print(_id)
        flashcard_deck.id = _id
        print("description: ", flashcard_deck.description)
        print(flashcard_deck.to_dynamo_dict())
        response = table.put_item(
            Item=flashcard_deck.to_dynamo_dict()
        )
        print('dynamo response: ', response)
        print('created deck')
        return get_by_id(_id)
    except ClientError as e:
        raise errors.ApiError(errors.internal_server_error, e)

    except errors.ApiError as e:
        raise e

    except Exception as e:
        errors.ApiError(errors.internal_server_error, e)
