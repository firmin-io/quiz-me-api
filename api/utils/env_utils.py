import logging

env = 'QA'

logging.getLogger().setLevel(logging.DEBUG)


def get_env():
    return env
