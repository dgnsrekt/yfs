from prompt_toolkit import prompt
from yfs.summary import get_summary_page
from time import time

while True:
    symbol = prompt(":> ").strip()
    if len(symbol) > 0:
        summary = get_summary_page(symbol, fuzzy_search=True, raise_error=False)
        if summary:
            print(summary.json(indent=4))
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
