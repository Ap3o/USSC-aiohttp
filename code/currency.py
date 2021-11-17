import exceptions
import redis_connector
import config

import os
import requests


def get_request_json(conv: str) -> requests.Request:
    try:
        request = requests.get(config.CURRCONV_LINK,
                               params={"q": conv, "compact": "ultra",
                                       "apiKey": os.getenv("CURRCONV_API_KEY")}).json()
    except TimeoutError as e:
        raise exceptions.USSCException("Невозможно обновить данные. Внешнее API недоступно.")
    return request


class Currencies:
    def __init__(self):
        self.cached_in_redis = []

    def set_new_currency(self, conv: str) -> None:
        request = get_request_json(conv)
        if conv not in request:
            # Вызываем ошибку для того чтобы исключить дальнейшую проверку в апи
            raise exceptions.USSCException(f"Пустой ответ от сервера {config.CURRCONV_LINK}")
        else:
            redis_connector.redis_instance.set(conv, request[conv])
            self.cached_in_redis.append(conv)

    def update_currency_data(self) -> None:
        # Из-за ограничения бесплатной версии отправляю запросы по одному.
        for value in self.cached_in_redis:
            request = get_request_json(value)
            redis_connector.redis_instance.set(value, request[value])

    def flush_db(self) -> None:
        redis_connector.redis_instance.flushdb(asynchronous=True)
        self.cached_in_redis = []


# Предустановленный объект, к которому будет обращаться views. (Отголоски Singleton шаблона)
currencies_instance = Currencies()
