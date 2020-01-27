import json


def build_response_with_body(status_code, response_body):
    return {
        "statusCode": status_code,
        "body": json.dumps(response_body)
    }
