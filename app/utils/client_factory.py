import redis
from app.utils.environment import redis_host, redis_port, redis_db


def get_redis_client():
    return redis.Redis(host=redis_host, port=redis_port, db=redis_db)
