import redis
import os

redis_instance = redis.StrictRedis(host=os.getenv("REDIS_HOST", "localhost"),
                                   port=os.getenv("REDIS_PORT", "6379"), db=0)


