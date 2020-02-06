import json


def build_response_with_body(status_code, response_body):
    return {
        "statusCode": status_code,
        "body": json.dumps(response_body)
    }


def build_response_without_body(status_code):
    return {
        "statusCode": status_code,
        "body": {}
    }
