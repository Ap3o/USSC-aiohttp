from aiohttp import web
from typing import NamedTuple

import exceptions
import redis_connector
import currency


class Conversion(NamedTuple):
    convert_from: str
    convert_to: str
    amount: float


# /convert/
async def convert(request: web.Request) -> web.Response:
    if request.method != "GET":
        return web.json_response({"error": "Wrong method"}, status=200)

    keys = ['from', 'to', 'amount']
    for key in keys:
        value = request.query.get(key)

        if value is None:
            return web.json_response({"error": f"{key} не указано!"}, status=200)

        # Обработка ошибки, если в amount передано не число.
        if key is 'amount':
            try:
                float(value)
            except ValueError as e:
                return web.json_response({"error": f"В поле {key} передано не число. {e}"}, status=200)

    new_conversion = Conversion(
        convert_from=request.query.get("from"),
        convert_to=request.query.get("to"),
        amount=float(request.query.get("amount")),
    )

    key = f"{new_conversion.convert_from}_{new_conversion.convert_to}"
    # Если такого ключа не будет в кэше, попробуем обратится к внешнему апи и узнать курс.
    if redis_connector.redis_instance.get(key) is None:
        # проверяем исключение при попытке добавить новую конвертацию
        try:
            currency.currencies_instance.set_new_currency(key)
        except exceptions.USSCException as e:
            return web.json_response(
                {
                    "error": f"Невозможно перевести валюту {new_conversion.convert_from} в {new_conversion.convert_to}. {e}"
                },
                status=200)

    result = new_conversion.amount * float(redis_connector.redis_instance.get(key))
    return web.json_response({"result": result}, status=200)


# /database/
async def database(request: web.Request) -> web.Response:
    if request.method != "POST":
        return web.json_response({"error": "Wrong method"})

    if "merge" not in request.query:
        return web.json_response({"error": "Не передано значение merge."})

    # Очистка данных из кэша
    if request.query["merge"] == "0":
        redis_connector.redis_instance.flushdb()
        return web.json_response({"result": "Данные очищены!"})

    # Обновление данных
    elif request.query["merge"] == "1":
        try:
            currency.currencies_instance.update_currency_data()
        except exceptions.USSCException as e:
            web.json_response({"error": e})
        return web.json_response({"result": "Данные обновлены."})
    else:
        return web.json_response({"error": f"Wrong merge value ({request.query['merge']})"})
