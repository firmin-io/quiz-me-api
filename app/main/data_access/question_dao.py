from app.main.data_access import dynamo_errors as de, dynamo_db as db
from botocore.exceptions import ClientError

from app.main.common import errors, validation
from app.main.model.model import QuestionModel
from app.main.utils.hash_utils import hash_password, check_password
from app.main.utils.id_utils import generate_id
from boto3.dynamodb.conditions import Key, Attr

table = db.dynamo_db.Table('qm_question')


def get_by_quiz_id(quiz_id, quietly=False):
    try:
        response = table.query(
            IndexName="quiz_id-index",
            KeyConditionExpression=Key('quiz_id').eq(quiz_id)
        )
        items = validation.validate_items_exist(response, quietly)
        questions = [QuestionModel.from_dynamo_json(question) for question in items if items]

        return questions

    except ClientError:
        raise errors.ApiError(errors.internal_server_error)

    except errors.ApiError as e:
        raise e

    except Exception as e:
        raise errors.ApiError(errors.internal_server_error)


def get_by_quiz_id_quietly(quiz_id):
    return get_by_quiz_id(quiz_id, True)


def get_by_id(_id):
    try:
        response = table.get_item(
            Key={
                'id': _id
            }
        )
        item = validation.validate_item_exists(response)
        return QuestionModel.from_dynamo_json(item)

    except ClientError:
        raise errors.ApiError(errors.internal_server_error)

    except errors.ApiError as e:
        raise e

    except Exception:
        raise errors.ApiError(errors.internal_server_error)


def create(question):
    try:
        _id = generate_id()
        question.id = _id
        table.put_item(
            Item=question.to_json()
        )
        return get_by_id(_id)

    except ClientError:
        raise errors.ApiError(errors.internal_server_error)

    except errors.ApiError as e:
        raise e

    except Exception:
        raise errors.ApiError(errors.internal_server_error)
