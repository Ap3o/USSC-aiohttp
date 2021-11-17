import redis
import os

redis_instance = redis.StrictRedis(host=os.getenv("REDIS_HOST"),
                                   port=os.getenv("REDIS_PORT"), db=0)


def flush_db():
    redis_instance.flushdb(asynchronous=True)
