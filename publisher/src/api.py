import redis
from environs import Env
from fastapi import FastAPI

from src.publishing import publish

env = Env()
env.read_env('.env')
CHANNEL = env('CHANNEL', default='test')
REDIS_HOST = env('REDIS_HOST', default='redis')
USERS_DB = 'users'

redis_client = redis.Redis(host=REDIS_HOST)
app = FastAPI()


@app.post('/message/send')
async def send_message(message: str):
    if publish(message):
        return {'status': 'Success'}, 200
    return {'status': 'Failed'}, 404


@app.post('/user/join')
async def join_user(user: str):
    if publish(user):
        redis_client.sadd(USERS_DB, user)
        return {'status': 'Success'}, 200
    return {'status': 'Failed'}, 404


@app.post('/user/remove')
async def remove_user(user: str):
    if publish(user):
        if redis_client.sismember(USERS_DB, user):
            redis_client.srem(USERS_DB, user)
            return {'status': 'Success'}, 200
    return {'status': 'Failed'}, 404
