from prompt_toolkit import prompt
from yfs.symbol import fuzzy_search

from time import time
from pprint import pprint

while True:
    print("Use 'exit' to end.")
    print("Type a symbol or company name.")
    symbol = prompt(":> ").strip()

    if len(symbol) > 0:
        result = fuzzy_search(symbol)

        if result:
            print(result.json(indent=4))

        else:
            print(symbol, "Not found")
