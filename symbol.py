from pydantic import BaseModel as Base
from pydantic import validator
from typing import Tuple, List, Dict, Optional, Callable
import requests
from requests_html import HTML
from pprint import pprint
from enum import Enum


BASE_URL = (
    "https://finance.yahoo.com/_finance_doubledown/api/resource/searchassist;searchTerm={symbol}"
)


class Item(Base):
    exch: str
    exchDisp: str
    name: str
    symbol: str
    type: str
    typeDisp: str


class SymbolAssistResponse(Base):
    hiConf: bool
    suggestionMeta: List[str]
    suggestionTitleAccessor: str
    items: List[Item]


for s in [
    "AAPL",
    "TSLA",
    "GOOGL",
    "overstock",
    "apple",
    "newegg",
    "sample",
    "nba",
    "nike",
    "ball",
    "sack",
    "queen",
]:
    resp = requests.get(BASE_URL.format(symbol=s))
    sar = SymbolAssistResponse(**resp.json())
    ALLOWED_EXCHANGES = ["NASDAQ", "NYSE"]
    # Needs enum. Then filter by allowed exchanges.
    sar.items = filter(lambda s: s.exchDisp in ALLOWED_EXCHANGES, sar.items)
    sar.items = filter(lambda s: s.typeDisp == "Equity", sar.items)

    for i in sar.items:
        print(i.symbol)
