import json
import requests
from config import exchanges


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')


        url = f"https://api.apilayer.com/exchangerates_data/convert?to={sym_key}&from={base_key}&amount={amount}"

        payload = {}
        headers = {
            "apikey": "pJHkcpcoKVaacW8TW3wcAv870X7f54Kw"
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        resp = json.loads(response.content)
        new_price = resp['result']

        return round(new_price, 2)


