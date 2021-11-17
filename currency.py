import redis_db
import requests

import config


def get_all_currency_methods() -> str:
    methods = ""
    for key in redis_db.redis_instance.keys():
        key = str(key)
        _ = key.split('_')
        methods += f"{_[0]} to {_[1]}\n"

    return methods


def get_currency():
    for conv in config.UPDATE_CONVERSION:
        req = requests.get(config.CURRCONV_LINK,
                           params={"q": conv, "compact": "ultra", "apiKey": config.CURRCONV_API_KEY}).json()

        redis_db.redis_instance.set(conv.replace('RUB', "RUR"), req[conv])


if __name__ == "__main__":
    get_currency()
