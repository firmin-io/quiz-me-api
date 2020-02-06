import json
import logging

from api.common import errors
from api.common.validation import validate_authorization_header_is_present
from api.data_access import question_dao, quiz_dao
from api.model.model import QuestionModel
from api.utils import auth_utils
from api.utils.api_utils import build_response_with_body, build_response_without_body


def create_question(event, context):
    print('creating question')
    try:
        token = validate_authorization_header_is_present(event['headers'])

        auth_utils.decode_auth_token(token)

        question_request = QuestionModel.from_request(json.loads(event['body']))
        validate_quiz_exists(question_request.quiz_id)
        return build_response_with_body(201, question_dao.create(question_request).to_dict())

    except errors.ApiError as ae:
        return errors.build_response_from_api_error(ae)

    except Exception as e:
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))


def update_question(event, context):
    try:
        token = validate_authorization_header_is_present(event['headers'])
        auth_utils.decode_auth_token(token)
        question_model = QuestionModel.from_update_request(json.loads(event['body']))
        quiz = question_dao.update(question_model)

        logging.debug(quiz)
        logging.debug(quiz.to_dict())

        return build_response_with_body(200, quiz.to_dict())

    except errors.ApiError as ae:
        return errors.build_response_from_api_error(ae)

    except Exception as e:
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))


def delete_question(event, context):
    try:
        token = validate_authorization_header_is_present(event['headers'])
        auth_utils.decode_auth_token(token)
        question_dao.delete(event['pathParameters']['question_id'])
        return build_response_without_body(204)

    except errors.ApiError as ae:
        return errors.build_response_from_api_error(ae)

    except Exception as e:
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))


def validate_quiz_exists(quiz_id):
    try:
        quiz = quiz_dao.get_by_id(quiz_id)
        logging.debug('quiz id {}'.format(quiz.id))
        return
    except errors.ApiError as e:
        if e.api_error.issue == 'NOT_FOUND':
            raise errors.ApiError(errors.invalid_quiz_id)
        return