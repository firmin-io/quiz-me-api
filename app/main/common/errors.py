

class Error:

    def __init__(self, issue, description, code, debug_id=None):
        self.issue = issue
        self.code = code
        self.description = description,
        self.debug_id = debug_id

    def to_json(self):
        if self.debug_id:
            return {
                'issue': self.issue,
                'description': self.description,
                'debug_id': self.debug_id
            }
        return {
            'issue': self.issue,
            'description': self.description
        }


class ApiError(Exception):

    def __init__(self, api_error, error=None):
        super(ApiError)
        self.api_error = api_error
        self.error = error


unauthorized = Error('UNAUTHORIZED', 'Authorization not provided or invalid', 401)

forbidden = Error('FORBIDDEN', 'The operation is forbidden', 403)

not_found = Error('NOT_FOUND', 'Unable to find the specified item(s)', 404)

internal_server_error = Error('INTERNAL_SERVER_ERROR', 'Unknown error', 500)

invalid_request_id = Error('BAD_REQUEST', 'The Request-Id header is missing or invalid', 400)

invalid_auth_token = Error('BAD_REQUEST', 'The Authorization header is missing or invalid', 400)

missing_required_param = Error('BAD_REQUEST', 'A required parameter is missing', 400)

failed_to_login = Error('UNPROCESSABLE_ENTITY', 'Failed to login', 422)

already_registered = Error('ALREADY_REGISTERED', 'An account exists for that email', 422)

invalid_email = Error('INVALID_EMAIL', 'The email is invalid', 400)


def build_response_from_api_error(ae, logger=None):
    if logger and ae.error:
        logger.log(ae.error)
        ae.api_error.debug_id = logger.debug_id

    return ae.api_error.to_json(), ae.api_error.code
