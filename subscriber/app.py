import logging
import time

import redis
from environs import Env

env = Env()
env.read_env('.env')

CHANNEL = env('CHANNEL', default='test')
REDIS_HOST = env('REDIS_HOST', default='redis')

logging.basicConfig(level=logging.DEBUG, format='%(levelname)-9s %(message)s', handlers=[logging.StreamHandler()])

logger = logging.getLogger(__file__)

if __name__ == '__main__':
    redis_client = redis.Redis(host=REDIS_HOST)
    pubsub = redis_client.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe(CHANNEL)

    while True:
        try:
            message = pubsub.get_message()
        except redis.ConnectionError as e:
            logger.error(f'Connection error: {e}')
        else:
            if message is not None:
                logger.info(f'Received message: {message}')
            else:
                time.sleep(0.1)
