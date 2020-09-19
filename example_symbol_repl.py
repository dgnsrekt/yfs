from prompt_toolkit import prompt

# from yfs.sum  mary import get_summary_page
from yfs.symbol import fuzzy_symbol_seach
from time import time
from pprint import pprint

while True:
    symbol = prompt(":> ").strip()

    if len(symbol) > 0:
        result = fuzzy_symbol_seach(symbol, first=True)
        if result:
            print(result.json(indent=4))
        else:
            print(symbol, "Not found")

# data = get_summary_page("GOOG", fuzzy_search=False, raise_error=False)
# print(data)
#
# print(tickers)
# print(tickers.json(indent=4))
# print(tickers.dict())
# print(tickers.dataframe.info())
# print(tickers.dataframe.describe())
