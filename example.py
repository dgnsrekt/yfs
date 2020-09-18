from pydantic import BaseModel as Base
from pydantic import validator, Field
from typing import Tuple, List, Dict, Optional
import requests
from requests_html import HTML
from pprint import pprint
from datetime import datetime
import more_itertools as mit

from collections import ChainMap
from pendulum.period import Period
from pendulum.date import Date
import pendulum

# yfs-terminal or yfs-repl
# yfs-rest

BASE_URL = "https://finance.yahoo.com/quote/{symbol}?p={symbol}"
SYMBOL = "DNKN"


class Cleaners:
    @staticmethod
    def remove_comma(value):
        return value.replace(",", "")

    @staticmethod
    def clean_percent_string(value):
        return value.replace("(", "").replace(")", "").replace("%", "")

    @staticmethod
    def check_data_missing(value):
        if value in ["N/A", "N/A (N/A)"]:
            return True
        else:
            return False


# Maybe have a quote section.
class Summary(Base, Cleaners):
    # Model which represents yf summary page.
    name: str
    close: Optional[float]
    change: Optional[float]
    percent_change: Optional[float]

    previous_close: Optional[float]
    open: Optional[float]

    bid_price: float = Field(alias="bid")
    bid_size: int = Field(alias="bid")

    ask_price: float = Field(alias="ask")
    ask_size: int = Field(alias="ask")

    days_range_open: float = Field(alias="days_range")
    days_range_close: float = Field(alias="days_range")

    fifty_two_week_range_open: float = Field(alias="fifty_two_week_range")
    fifty_two_week_range_close: float = Field(alias="fifty_two_week_range")

    volume: Optional[int]
    average_volume: Optional[int] = Field(alias="avg_volume")

    market_cap: Optional[int]
    beta_five_year_monthly: Optional[float]
    pe_ratio_ttm: Optional[float]
    eps_ttm: Optional[float]

    earnings_date: Optional[Period]

    forward_dividend_yield: Optional[float]
    forward_dividend_yield_percentage: Optional[float] = Field(alias="forward_dividend_yield")
    exdividend_date: Optional[Date]

    one_year_target_est: Optional[float]

    class Config:
        json_encoders = {Period: lambda period: str(period)}

    @validator(
        "close",
        "previous_close",
        "open",
        "volume",
        "average_volume",
        "pe_ratio_ttm",
        "beta_five_year_monthly",
        pre=True,
    )
    def clean_value(cls, value):
        if cls.check_data_missing(value):
            return None
        else:
            return cls.remove_comma(value)

    @validator("change", "forward_dividend_yield", pre=True)
    def clean_change(cls, value):
        if cls.check_data_missing(value):
            return None
        else:
            return value.split(" ")[0]

    @validator("percent_change", "forward_dividend_yield_percentage", pre=True)
    def clean_percent_change(cls, value):
        if cls.check_data_missing(value):
            return None
        else:
            value = value.split(" ")[1]
            return cls.clean_percent_string(value)

    @validator("bid_price", "ask_price", pre=True)
    def clean_book_price(cls, value):
        if cls.check_data_missing(value):
            return None
        else:
            price, _ = value.split("x")
            return price

    @validator("bid_size", "ask_size", pre=True)
    def clean_book_size(cls, value):
        if cls.check_data_missing(value):
            return None
        else:
            _, size = value.split("x")
            return size

    @validator("days_range_open", "fifty_two_week_range_open", pre=True)
    def clean_range_start(cls, value):
        if cls.check_data_missing(value):
            return None
        else:
            value = cls.remove_comma(value)
            start, _ = value.split("-")
            return start

    @validator("days_range_close", "fifty_two_week_range_close", pre=True)
    def clean_range_end(cls, value):
        if cls.check_data_missing(value):
            return None
        else:
            value = cls.remove_comma(value)
            _, end = value.split("-")
            return end

    @validator("market_cap", pre=True)
    def clean_market_cap(cls, value):
        if cls.check_data_missing(value):
            return None
        else:
            cap = dict()

            cap["T"] = 1_000_000_000_000
            cap["B"] = 1_000_000_000
            cap["M"] = 1_000_000

            for c, v in cap.items():
                if c in value:
                    return round(float(value.replace(c, "")) * v)
            else:
                return round(float(value))

    @validator("earnings_date", pre=True)
    def clean_date_range(cls, dates):
        if cls.check_data_missing(dates):
            return None
        else:
            start, end = dates.split("-")

            start = pendulum.parse(start, strict=False)
            end = pendulum.parse(end, strict=False)

            period = end - start
            return period

    @validator("exdividend_date", pre=True)
    def clean_date(cls, date):
        if cls.check_data_missing(date):
            return None
        else:
            return pendulum.parse(date, strict=False)


class QuoteHeaderInfoSelectors(Base):  # quote_header_info_selectors
    name: str = ".D\(ib\).Fz\(18px\)"
    close: str = ".Trsdu\(0\.3s\).Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)"
    percent_change: str = ".Trsdu\(0\.3s\).Fw\(500\)"
    change: str = ".Trsdu\(0\.3s\).Fw\(500\)"


resp = requests.get(BASE_URL.format(symbol=SYMBOL))

html = HTML(html=resp.text)


header_selectors = QuoteHeaderInfoSelectors()

quote_header_info = html.find("div#quote-header-info", first=True)

if quote_header_info:

    data = {}
    for name, value in header_selectors:

        element = quote_header_info.find(value)

        if element and len(element) == 1:
            data[name] = element[0].text

    quote_summary = html.find("div#quote-summary", first=True)
    element = quote_summary.find("tr")
    tr = [el.text.split("\n") for el in element]

    def table_cleaner(k):
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
        x = table_cleaner(x)
        more_data[x] = y

    data = ChainMap(data, more_data)
    print(data)
    summary = Summary(**data)
    print(summary.dict())
    print(summary.json(indent=4))

# if quote_header_info:
# print(quote_header_info.find(close_selector, first=True).text)


# s = Summary(previous_close="1508.83")
# print(s)
