from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from app.main.common import errors, validation
from app.main.data_access import dynamo_db as db, question_dao
from app.main.model.model import QuizModel
from app.main.utils.id_utils import generate_id

table = db.dynamo_db.Table('qm_quiz')


def get_by_user_id(user_id):
    try:
        response = table.query(
            IndexName="user_id-index",
            KeyConditionExpression=Key('user_id').eq(user_id)
        )
        items = validation.validate_items_exist_quietly(response)
        quizzes = []
        for item in items:
            quiz = QuizModel.from_dynamo_json(item)
            questions = question_dao.get_by_quiz_id_quietly(quiz.id)
            quiz.questions = questions
            quizzes.append(quiz)

        return quizzes

    except ClientError:
        raise errors.ApiError(errors.internal_server_error)

    except errors.ApiError as e:
        raise e

    except Exception as e:
        errors.ApiError(errors.internal_server_error, e)


def get_by_id(_id):
    try:
        print('getting quiz by id')
        response = table.get_item(
            Key={
                'id': _id
            }
        )
        print('got quiz by id')
        item = validation.validate_item_exists(response)
        print('got item')
        quiz = QuizModel.from_dynamo_json(item)
        print(quiz)
        questions = question_dao.get_by_quiz_id_quietly(quiz.id)
        quiz.questions = questions
        return quiz

    except ClientError:
        raise errors.ApiError(errors.internal_server_error)

    except errors.ApiError as e:
        raise e

    except Exception as e:
        errors.ApiError(errors.internal_server_error, e)


def create(quiz):
    try:
        _id = generate_id()
        quiz.id = _id
        table.put_item(
            Item=quiz.to_json(True)
        )
        return get_by_id(_id)
    except ClientError as e:
        raise errors.ApiError(errors.internal_server_error, e)

    except errors.ApiError as e:
        raise e

    except Exception as e:
        errors.ApiError(errors.internal_server_error, e)
