import logging

env = 'PROD'

logging.getLogger().setLevel(logging.DEBUG)


def get_env():
    return env
