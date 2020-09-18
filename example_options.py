from yfs.symbol import FuzzySymbolSearch

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

import pandas
from pandas import DataFrame

TICKERS = ["TSLA", "AAPL", "GOOGLE", "FCEL"]

from time import time

symbol = TICKERS[3]
url = f"https://finance.yahoo.com/quote/BYND/options?p={symbol}"
resp = requests.get(url)
html = HTML(html=resp.text, url=url)
el = html.find("div.Fl\(start\).Pend\(18px\)", first=True)
for o in el.find("option"):
    print(o.attrs["value"])


# start = time()
# tickers = get_summary_pages(TICKERS, fuzzy_search=True, with_threads=False)
# end = time()
# print("no threads")
# print(end - start)
