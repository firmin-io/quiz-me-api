import json
import logging

from api.common import errors
from api.common.validation import validate_authorization_header_is_present, validate_user_exists_by_id
from api.data_access import quiz_dao
from api.model.model import QuizModel
from api.utils import auth_utils
from api.utils.api_utils import build_response_with_body, build_response_without_body


def create_quiz(event, context):
    try:
        token = validate_authorization_header_is_present(event['headers'])
        auth_utils.decode_auth_token(token)
        quiz_request = QuizModel.from_request(json.loads(event['body']))
        logging.debug(quiz_request.user_id)
        validate_user_exists_by_id(quiz_request.user_id)
        quiz = quiz_dao.create(quiz_request)

        logging.debug(quiz)
        logging.debug(quiz.to_dict())

        return build_response_with_body(201, quiz.to_dict())

    except errors.ApiError as ae:
        return errors.build_response_from_api_error(ae)

    except Exception as e:
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))


def get_quiz_by_id(event, context):
    try:
        token = validate_authorization_header_is_present(event['headers'])
        auth_utils.decode_auth_token(token)
        quiz = quiz_dao.get_by_id(event['pathParameters']['quiz_id'])

        print('********* getting quiz')

        logging.debug(quiz)
        logging.debug(quiz.to_dict())

        return build_response_with_body(200, quiz.to_dict())

    except errors.ApiError as ae:
        return errors.build_response_from_api_error(ae)

    except Exception as e:
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))


def get_by_user_id(event, context):
    try:
        logging.debug('event headers: ', event['headers'])
        token = validate_authorization_header_is_present(event['headers'])
        auth_utils.decode_auth_token(token)

        items = quiz_dao.get_by_user_id(event['pathParameters']['user_id'])

        quizzes = [item.to_dict() for item in items if items]

        return build_response_with_body(200, quizzes)

    except errors.ApiError as ae:
        return errors.build_response_from_api_error(ae)

    except Exception as e:
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))


def update_quiz(event, context):
    try:
        token = validate_authorization_header_is_present(event['headers'])
        auth_utils.decode_auth_token(token)
        quiz_request = QuizModel.from_update_request(json.loads(event['body']))
        quiz = quiz_dao.update(quiz_request)

        logging.debug(quiz)
        logging.debug(quiz.to_dict())

        return build_response_with_body(200, quiz.to_dict())

    except errors.ApiError as ae:
        return errors.build_response_from_api_error(ae)

    except Exception as e:
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))


def get_quizzes(event, context):
    try:
        items = quiz_dao.get_all()
        quizzes = [item.to_dict() for item in items if items]
        return build_response_with_body(200, quizzes)

    except errors.ApiError as ae:
        return errors.build_response_from_api_error(ae)

    except Exception as e:
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))


def delete_quiz(event, context):
    try:
        token = validate_authorization_header_is_present(event['headers'])
        auth_utils.decode_auth_token(token)
        quiz_dao.delete(event['pathParameters']['quiz_id'])
        return build_response_without_body(204)

    except errors.ApiError as ae:
        return errors.build_response_from_api_error(ae)

    except KeyError as e:
        return errors.build_response_from_api_error(errors.Error('MISSING_REQUIRED_PARAMETER', str(e), 400))

    except Exception as e:
        return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))
