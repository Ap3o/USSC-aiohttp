import redis
import config

redis_instance = redis.StrictRedis(host=config.REDIS_HOST,
                                   port=config.REDIS_PORT, db=0)

# Начальные данные на момент разработки (17.11.2021 19:13 EKB)
redis_instance.set("RUR_USD", 0.013811)
redis_instance.set("USD_RUR", 72.404001)


def flush_db():
    redis_instance.flushdb(asynchronous=True)
