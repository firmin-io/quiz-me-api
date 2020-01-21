import re

from flask import request
from flask_restful import Resource

from app.main.common import errors
from app.main.common.validation import validate_authorization_header_is_present
from app.main.data_access import question_dao, quiz_dao
from app.main.model.model import QuizModel, QuestionModel
from app.main.utils import auth_utils, id_utils, logging_utils


class QuestionsResource(Resource):

    def post(self):
        logger = logging_utils.ApiLogger(id_utils.generate_debug_id())
        try:
            token = validate_authorization_header_is_present(request)
            auth_utils.decode_auth_token(token)
            question_request = QuestionModel.from_request_json(request.json)
            validate_quiz_exists(question_request.quiz_id)
            return question_dao.create(question_request).to_json(), 201

        except errors.ApiError as ae:
            return errors.build_response_from_api_error(ae, logger)

        except Exception as e:
            return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e), logger)

    def get(self):
        return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))

    def put(self):
        return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))

    def delete(self):
        return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))


class QuestionResource(Resource):

    def get(self):
        return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))

    def post(self):
        return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))

    # TODO
    def put(self):
        return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))

    # TODO
    def delete(self):
        return errors.build_response_from_api_error(errors.ApiError(errors.forbidden))


def validate_quiz_exists(quiz_id):
    try:
        quiz = quiz_dao.get_by_id(quiz_id)
        print('quiz id {}'.format(quiz.id))
        return
    except errors.ApiError as e:
        if e.api_error.issue == 'NOT_FOUND':
            raise errors.ApiError(errors.invalid_quiz_id)
        return
