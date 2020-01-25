from flask import request
from flask_restful import Resource

from api.common import errors
from api.common.validation import validate_authorization_header_is_present
from api.data_access import question_dao, quiz_dao
from api.model.model import QuestionModel
from api.utils import auth_utils


class QuestionsResource(Resource):

    def post(self):
        try:
            token = validate_authorization_header_is_present(request)
            auth_utils.decode_auth_token(token)
            question_request = QuestionModel.from_request_json(request.json)
            validate_quiz_exists(question_request.quiz_id)
            return question_dao.create(question_request).to_dict(), 201

        except errors.ApiError as ae:
            return errors.build_response_from_api_error(ae)

        except Exception as e:
            return errors.build_response_from_api_error(errors.ApiError(errors.internal_server_error, e))

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
