import uuid


def generate_id():
    return str(uuid.uuid4())


def generate_debug_id():
    return 'di-{}'.format(generate_id())

