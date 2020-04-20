import uuid
from time import gmtime, strftime

import time_uuid


def generate_timestamp():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())


def generate_time_uuid():
    t_id = str(time_uuid.TimeUUID.with_timestamp(time_uuid.utctime()))
    formatted_id = t_id[14:19] + t_id[9:14] + t_id[0:9] + t_id[19:]
    return formatted_id[0:18] + str(uuid.uuid4())[18:]

