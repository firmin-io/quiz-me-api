import json

from api.common import errors
from api.common.validation import validate_authorization_header_is_present
from api.data_access import question_dao, quiz_dao
from api.model.model import QuestionModel
from api.utils import auth_utils


def create_question(event, context):
    try:
        token = validate_authorization_header_is_present(event['headers'])
        auth_utils.decode_auth_token(token)
        question_request = QuestionModel.from_request_json(json.loads(event['body']))
        validate_quiz_exists(question_request.quiz_id)
        return question_dao.create(question_request).to_dict(), 201

    except errors.ApiError as ae:
        return errors.build_response_from_api_error(ae)

    except Exception as e:
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))


def validate_quiz_exists(quiz_id):
    try:
        quiz = quiz_dao.get_by_id(quiz_id)
        print('quiz id {}'.format(quiz.id))
        return
    except errors.ApiError as e:
        if e.api_error.issue == 'NOT_FOUND':
            raise errors.ApiError(errors.invalid_quiz_id)
        return


def update_question(event, context):
    # TODO
    pass


def delete_question(event, context):
    # TODO
    pass
