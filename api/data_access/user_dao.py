import logging

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from api.common import errors, validation
from api.data_access import dynamo_db as db
from api.model.model import UserModel
from api.utils.hash_utils import hash_password
from api.utils.id_utils import generate_id

table = db.dynamo_db.Table('qm_user')


def get_by_email(email):

    try:
        response = table.query(
            IndexName="email-index",
            KeyConditionExpression=Key('email').eq(email)
        )
        logging.debug('dynamo response: ')
        logging.debug(response)
        item = validation.validate_items_exist(response)[0]
        return UserModel.from_dynamo(item)
    except ClientError:
        raise errors.ApiError(errors.internal_server_error)

    except Exception as e:
        if str(e) == 'list index out of range':
            print(e)
            raise errors.ApiError(errors.not_found)
        else:
            raise errors.ApiError(errors.internal_server_error, e)


def get_by_id(_id):
    try:
        logging.debug('retrieve user by id')
        response = table.get_item(
            Key={
                'id': _id
            }
        )
        logging.debug('dynamo response: ', response)
        item = validation.validate_item_exists(response)
        return UserModel.from_dynamo(item)
    except ClientError as e:
        logging.debug(e)
        raise errors.ApiError(errors.internal_server_error)


def create(user):
    logging.debug('creating user...')
    try:
        _id = generate_id()
        logging.debug('id generated')
        user.id = _id
        user.password = hash_password(user.password)
        logging.debug('hash generated')
        table.put_item(
            Item=user.to_dynamo_dict()
        )
        logging.debug('success creating user')
        return get_by_id(_id)
    except ClientError as e:
        logging.debug(e)
        logging.debug(str(e))
        raise errors.ApiError(errors.internal_server_error)
    except Exception as e:
        logging.debug(e)
        logging.debug(str(e))
        raise errors.ApiError(errors.internal_server_error)
