from app.main.data_access import dynamo_errors as de, dynamo_db as db
from botocore.exceptions import ClientError

from app.main.common import errors, validation
from app.main.model.model import QuizModel
from app.main.utils.hash_utils import hash_password, check_password
from app.main.utils.id_utils import generate_id
from boto3.dynamodb.conditions import Key, Attr

from app.main.data_access import question_dao

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


def get_by_id(_id):
    try:
        response = table.get_item(
            Key={
                'id': _id
            }
        )
        item = validation.validate_item_exists(response)
        print(item)
        quiz = QuizModel.from_dynamo_json(item)
        print(quiz)
        questions = question_dao.get_by_quiz_id(quiz.id, True)
        quiz.questions = questions
        return quiz
    except ClientError:
        raise errors.ApiError(errors.internal_server_error)


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
    except Exception as e:
        raise errors.ApiError(errors.internal_server_error, e)
