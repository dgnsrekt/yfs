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
US_EXCHANGES = ["NASDAQ", "NYSE"]


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

    def update_items(items: List[Item]):
        self.items = items


def FuzzySymbolSearch(symbol, session=None):
    if session:
        response = session.get(BASE_URL.format(symbol=symbol))
    else:
        response = requests.get(BASE_URL.format(symbol=symbol))

    if response.ok:
        sar = SymbolAssistResponse(**response.json())

        filtered_items = filter(lambda s: s.exchDisp in US_EXCHANGES, sar.items)
        filtered_items = list(filter(lambda s: s.typeDisp == "Equity", filtered_items))

        if filtered_items:
            return filtered_items[0]

    return None
