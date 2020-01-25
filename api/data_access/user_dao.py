from api.data_access import dynamo_db as db
from botocore.exceptions import ClientError

from api.common import validation, errors
from api.model.model import UserModel

from boto3.dynamodb.conditions import Key

from api.utils.hash_utils import hash_password
from api.utils.id_utils import generate_id

table = db.dynamo_db.Table('qm_user')


def get_by_email(email):

    try:
        response = table.query(
            IndexName="email-index",
            KeyConditionExpression=Key('email').eq(email)
        )
        print('dynamo response: ')
        print(response)
        item = validation.validate_items_exist(response)[0]
        return UserModel.from_dynamo_json(item)
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
        return UserModel.from_dynamo_json(item)
    except ClientError:
        raise errors.ApiError(errors.internal_server_error)


def create(user):
    try:
        _id = generate_id()
        user.id = _id
        user.password = hash_password(user.password)
        table.put_item(
            Item=user.to_dict()
        )
        return get_by_id(_id)
    except ClientError:
        raise errors.ApiError(errors.internal_server_error)
    except Exception as e:
        raise errors.ApiError(errors.internal_server_error)
