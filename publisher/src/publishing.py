import logging

import redis
from environs import Env

env = Env()
env.read_env('.env')
CHANNEL = env('CHANNEL', default='test')
REDIS_HOST = env('REDIS_HOST', default='redis')


def publish(message: str) -> bool:
    try:
        publish_result = redis.Redis(host=REDIS_HOST).publish(CHANNEL, message)
        if publish_result > 0:
            return True
    except redis.ConnectionError as e:
        logging.error(f'Will attempt to retry, {e}')
    except Exception as e:
        logging.error(f'Other exception, {e}')

    return False
