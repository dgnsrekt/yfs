from yfs.symbol import fuzzy_symbol_seach

from pydantic import BaseModel as Base
from pydantic import validator, Field

from typing import Tuple, List, Dict, Optional, Union

import requests
from requests import Session
from requests_html import HTML

from collections import ChainMap

import pendulum
from pendulum.period import Period
from pendulum.date import Date
from pendulum.datetime import DateTime

import pandas
from pandas import DataFrame
from time import time

from pprint import pprint

from itertools import cycle

from enum import Enum

TICKERS = ["TSLA", "AAPL", "GOOGLE", "FCEL"]

symbol = "BYND"


class OptionContracts(Base):
    symbol: str
    expirations: List[DateTime]

    @validator("expirations", pre=True)
    def sort_dates(cls, values):
        return sorted(values)

    def filter_after(self, filter_date: DateTime):
        filtered = list(filter(lambda date_: date_ >= filter_date, self.expirations))
        return OptionContracts(symbol=self.symbol, expirations=filtered)

    def __iter__(self):
        return iter(self.expirations)


class OptionType(str, Enum):
    CALL = "CALL"
    PUT = "PUT"


class Option(Base):
    symbol: str
    expiration: DateTime

    type: OptionType

    contract_name: str
    # last_trade_date: DateTime
    strike: float
    last_price: float
    bid: float
    ask: float
    change: float
    percent_change: float
    volume: int
    open_interest: int
    implied_volatility: float
    in_the_money: bool

    @validator("strike", "bid", "ask", "change", pre=True)
    def cleanly(cls, value):
        return value.replace(",", "")

    @validator("implied_volatility", pre=True)
    def clean_value(cls, value):
        return value.replace("(", "").replace(")", "").replace("%", "").replace(",", "")

    @validator("percent_change", "volume", "open_interest", pre=True)
    def clean_percent_change(cls, value):
        if value == "-":
            return 0.0
        else:
            value = value.replace("-", "").replace("%", "").replace(",", "")
            return value


class Options(Base):
    options: List[Option]  # expiration and contracts maybe.


def get_option_expirations(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}/options?p={symbol}"
    response = requests.get(url)

    html = HTML(html=response.text, url=url)

    elements = html.find("div.Fl\(start\).Pend\(18px\)", first=True)

    timestamps = [element.attrs["value"] for element in elements.find("option")]

    dates = [pendulum.from_timestamp(int(timestamp)) for timestamp in timestamps]

    dates = OptionContracts(symbol=symbol, expirations=dates)

    return dates


x = get_option_expirations("SPY")

print(x.json(indent=4))

filter_date = pendulum.now().add(days=45)

other = x.filter_after(filter_date=filter_date)


def table_header_cleaner(header):
    return header.lower().replace(" ", "_").replace("%", "percent")


pack = []
for exp in other:
    symbol = other.symbol
    contract_timestamp = exp.int_timestamp

    url = f"https://finance.yahoo.com/quote/{symbol}/options?date={contract_timestamp}&p={symbol}"
    response = requests.get(url)

    html = HTML(html=response.text, url=url)

    call_option_table = html.find("table.calls", first=True)
    put_option_table = html.find("table.puts", first=True)

    head = call_option_table.find("thead", first=True)
    body = call_option_table.find("tbody", first=True)

    headers = cycle(head.text.split("\n"))

    for row in body.find("tr"):
        d = {"symbol": symbol, "expiration": exp, "type": "CALL"}

        if "in-the-money" in row.attrs["class"]:
            d["in_the_money"] = True
        else:
            d["in_the_money"] = False

        for col in row.text.split("\n"):
            h = table_header_cleaner(next(headers))
            # print(h, col)
            d[h] = col

        print(".", end="", flush=True)
        pack.append(Option(**d))

    break

print(len(pack))
calls = Options(options=pack).dict()
print(DataFrame.from_dict(calls["options"]).to_string())

# for h in header:
# print(h)
# break
