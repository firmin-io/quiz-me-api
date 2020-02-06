import logging

from environs import Env

env = Env()
env.read_env()


logging.getLogger().setLevel(logging.DEBUG)

def get_env():
    return env('ENV')