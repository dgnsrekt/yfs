from yfs.summary import get_summary_page, get_summary_pages

TICKERS = [
    "TSLA",
    "AAPL",
    "GOOGLE",
    "FCEL",
    "BALL_SACK_CITY",
    "NOT A GOOD COMPANY",
    "GOOG",
    "WTF",
    "LEVI",
    "LEVIS",
    "BEYOND MEAT",
    "MEAT CITY",
    "RANDOM",
    "GOOGL",
]

from time import time

data = get_summary_page("GOOG", fuzzy_search=False, raise_error=False)
print(data)

# start = time()
# tickers = get_summary_pages(TICKERS, fuzzy_search=True, with_threads=False)
# end = time()
# print("no threads")
# print(end - start)

start = time()
tickers = get_summary_pages(TICKERS, fuzzy_search=True, with_threads=True)
end = time()
print("with threads")
print(end - start)


print(tickers)
print(tickers.json(indent=4))
print(tickers.dict())
print(tickers.dataframe.info())
print(tickers.dataframe.describe())
