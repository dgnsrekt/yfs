from pydantic import BaseModel as Base
from pydantic import validator
from typing import Tuple, List, Dict, Optional
import requests
from requests_html import HTML
from pprint import pprint
from datetime import datetime
import more_itertools as mit

from collections import ChainMap

# yfs-terminal or yfs-repl
# yfs-rest

BASE_URL = "https://finance.yahoo.com/quote/{symbol}?p={symbol}"

# Maybe have a quote section.
class Summary(Base):
    # Model which represents yf summary page.
    name: str
    close: float
    change: float
    percent_change: float

    previous_close: float
    open: float
    bid: Tuple[float, int]
    ask: Tuple[float, int]
    days_range: Tuple[float, float]
    fifty_two_week_range: Tuple[float, float]
    volume: int
    avg_volume: int

    @validator("close", "previous_close", "open", pre=True)
    def clean_value(cls, value):
        return value.replace(",", "")

    #
    @validator("change", pre=True)
    def validate_change(cls, v):
        return v.split(" ")[0]

    @validator("percent_change", pre=True)
    def validate_percent_change(cls, v):
        return v.split(" ")[1].replace("(", "").replace(")", "").replace("%", "")

    @validator("bid", "ask", pre=True)
    def clean_bid_ask(cls, values):
        price, amount = values.split("x")
        return price, amount

    @validator("days_range", "fifty_two_week_range", pre=True)
    def clean_range(cls, value):
        start, end = value.replace(",", "").split("-")
        return start, end

    @validator("volume", "avg_volume", pre=True)
    def clean_volume(cls, value):
        return value.replace(",", "")


class QuoteHeaderInfoSelectors(Base):  # quote_header_info_selectors
    name: str = ".D\(ib\).Fz\(18px\)"
    close: str = ".Trsdu\(0\.3s\).Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)"
    percent_change: str = ".Trsdu\(0\.3s\).Fw\(500\)"
    change: str = ".Trsdu\(0\.3s\).Fw\(500\)"


resp = requests.get(BASE_URL.format(symbol="AAPL"))

html = HTML(html=resp.text)


header_selectors = QuoteHeaderInfoSelectors()

quote_header_info = html.find("div#quote-header-info", first=True)
data = {}
for name, value in header_selectors:

    element = quote_header_info.find(value)

    if element and len(element) == 1:
        data[name] = element[0].text


quote_summary = html.find("div#quote-summary", first=True)
element = quote_summary.find("tr")
tr = [el.text.split("\n") for el in element]


def cleaner(k):
    return (
        k.lower()
        .replace("(", "")
        .replace(")", "")
        .replace("'", "")
        .replace(".", "")
        .replace("& ", "")
        .replace("-", "")
        .replace("52", "fifty_two")
        .replace("5y", "five_year")
        .replace("1y", "one_year")
        .replace(" ", "_")
    )


more_data = {}
for x, y in tr:
    x = cleaner(x)
    more_data[x] = y

# print(data)
data = ChainMap(data, more_data)
print(data)
summary = Summary(**data)
print(summary.json(indent=4))
# if quote_header_info:
# print(quote_header_info.find(close_selector, first=True).text)


# s = Summary(previous_close="1508.83")
# print(s)
