from aiohttp import web
from typing import NamedTuple

import redis_db
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
        convert_from=request.query.get(keys[0]),
        convert_to=request.query.get(keys[1]),
        amount=float(request.query.get(keys[2])),
    )

    key = f"{new_conversion.convert_from}_{new_conversion.convert_to}"
    if len(redis_db.redis_instance.keys()) > 0:
        pass
    else:
        return web.json_response({"error": "База на сервере пуста. Невозможно конвертировать валюту."}, status=200)
    # Если такого ключа не будет в кэше, значит валюту нельзя перевести.
    if redis_db.redis_instance.get(key) is None:
        all_currency_methods = currency.get_all_currency_methods()
        return web.json_response(
            {
                "error": f"Невозможно перевести валюту {new_conversion.convert_from} в {new_conversion.convert_to}."
                         f"Доступные варианты:  {all_currency_methods}"},
            status=200)

    result = new_conversion.amount * float(redis_db.redis_instance.get(key))
    return web.json_response({"result": result}, status=200)


# /database/
async def database(request: web.Request) -> web.Response:
    if request.method != "POST":
        return web.json_response({"error": "Wrong method"})

    # Очистка данных из кэша
    if request.query["merge"] == "0":
        redis_db.redis_instance.flushdb()
        return web.json_response({"result": "Данные очищены!"})

    # Перетарание данных
    elif request.query["merge"] == "1":
        currency.get_currency()
        return web.json_response({"result": "Данные перетерты."})
    else:
        return web.json_response({"error": f"Wrong merge value ({request.query['merge']})"})
