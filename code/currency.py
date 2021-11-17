import exceptions
import redis_db
import config

import os
import requests


def set_new_currency(conv):
    req = requests.get(config.CURRCONV_LINK,
                       params={"q": conv, "compact": "ultra", "apiKey": os.getenv("CURRCONV_API_KEY")}).json()

    if conv not in req:
        # Вызываем ошибку для того чтобы исключить дальнейшую проверку в апи
        raise exceptions.USSCException(f"Пустой ответ от сервера {config.CURRCONV_LINK}")
    else:
        redis_db.redis_instance.set(conv, req[conv])
