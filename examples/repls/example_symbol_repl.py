from prompt_toolkit import prompt
from yfs.lookup import fuzzy_search

from time import time
from pprint import pprint
from pydantic import BaseModel as Base
from yfs.exchanges import ExchangeTypes

ExchangeTypes.show()

while True:
    print("Use 'exit' to end.")
    print("Type a symbol or company name.")

    symbol = prompt(":> ").strip()

    if len(symbol) > 0:
        result = fuzzy_search(symbol, exchange_type=ExchangeTypes.united_states)

        if result:
            print(result.json(indent=4))

        else:
            print(symbol, "Not found")
