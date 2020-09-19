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

from yfs.symbol import fuzzy_symbol_seach
import enlighten

JSON_ENCODERS = {Period: lambda period: f"{str(period.start.date())} {str(period.end.date())}"}


class Cleaners:
    @staticmethod
    def remove_comma(value):
        return value.replace(",", "")

    @staticmethod
    def clean_percent_string(value):
        return value.replace("(", "").replace(")", "").replace("%", "")

    @staticmethod
    def check_data_missing(value):
        if value in [
            "N/A",
            "N/A (N/A)",
            "N/A x N/A",
            "N/A - N/A",
            "undefined - undefined",
            " ",
            "",
        ]:
            return True
        else:
            return False


class Summary(Base, Cleaners):
    # Model which represents yf summary page.
    symbol: str
    name: str

    open: Optional[float]
    high: Optional[float] = Field(alias="days_range")
    low: Optional[float] = Field(alias="days_range")
    close: Optional[float]

    change: Optional[float]
    percent_change: Optional[float]

    previous_close: Optional[float]

    bid_price: Optional[float] = Field(alias="bid")
    bid_size: Optional[int] = Field(alias="bid")

    ask_price: Optional[float] = Field(alias="ask")
    ask_size: Optional[int] = Field(alias="ask")

    fifty_two_week_low: Optional[float] = Field(alias="fifty_two_week_range")
    fifty_two_week_high: Optional[float] = Field(alias="fifty_two_week_range")

    volume: Optional[int]
    average_volume: Optional[int] = Field(alias="avg_volume")

    market_cap: Optional[int]

    beta_five_year_monthly: Optional[float]
    pe_ratio_ttm: Optional[float]
    eps_ttm: Optional[float]

    earnings_date: Optional[Union[Period, Date]]

    forward_dividend_yield: Optional[float]
    forward_dividend_yield_percentage: Optional[float] = Field(alias="forward_dividend_yield")
    exdividend_date: Optional[Date]

    one_year_target_est: Optional[float]

    class Config:
        json_encoders = JSON_ENCODERS

    @validator(
        "close",
        "previous_close",
        "open",
        "volume",
        "average_volume",
        "pe_ratio_ttm",
        "beta_five_year_monthly",
        "one_year_target_est",
        "eps_ttm",
        pre=True,
    )
    def clean_value(cls, value):
        if cls.check_data_missing(value):
            return None
        else:
            return cls.remove_comma(value)

    @validator("symbol")
    def clean_symbol(cls, value):
        return value.upper()

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
            return cls.remove_comma(price)

    @validator("bid_size", "ask_size", pre=True)
    def clean_book_size(cls, value):
        if cls.check_data_missing(value):
            return None
        else:
            _, size = value.split("x")
            return size  # NOTE: strip?

    @validator("low", "fifty_two_week_low", pre=True)
    def clean_range_start(cls, value):
        if cls.check_data_missing(value):
            return None
        else:
            value = cls.remove_comma(value)
            start, _ = value.split("-")
            return start

    @validator("high", "fifty_two_week_high", pre=True)
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
    def clean_date_range(cls, value):
        if cls.check_data_missing(value):
            return None

        dates = value.split("-")

        if len(dates) > 1:
            start, end = dates

            start = pendulum.parse(start, strict=False)
            end = pendulum.parse(end, strict=False)

            period = end - start
            return period
        else:
            return pendulum.parse(value, strict=False)

    @validator("exdividend_date", pre=True)
    def clean_date(cls, date):
        if cls.check_data_missing(date):
            return None
        else:
            return pendulum.parse(date, strict=False)


class SummaryGroup(Base):
    data: List[Summary]

    class Config:
        json_encoders = JSON_ENCODERS

    @property
    def symbols(self):
        return [symbol.symbol for symbol in self]

    @property
    def dataframe(self, sorted=True):
        data = self.dict()
        dataframe = DataFrame.from_dict(data["data"])
        dataframe.set_index("symbol", inplace=True)
        if sorted:
            dataframe.sort_index(inplace=True)
        return dataframe  # TODO: none or nan

    def __iter__(self):
        return iter(self.data)


class QuoteHeaderInfoSelectors(Base):
    name: str = ".D\(ib\).Fz\(18px\)"
    close: str = ".Trsdu\(0\.3s\).Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)"
    percent_change: str = ".Trsdu\(0\.3s\).Fw\(500\)"
    change: str = ".Trsdu\(0\.3s\).Fw\(500\)"


def parse_header(html):
    header_selectors = QuoteHeaderInfoSelectors()

    quote_header_info = html.find("div#quote-header-info", first=True)

    data = {}

    if quote_header_info:

        for name, value in header_selectors:
            element = quote_header_info.find(value)

            if element and len(element) == 1:
                data[name] = element[0].text

    if data:
        return data
    else:
        return None


def table_key_cleaner(key):
    return (
        key.lower()
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


def parse_summary_table(html):
    quote_summary = html.find("div#quote-summary", first=True)

    if quote_summary:

        table_rows = quote_summary.find("tr")

        rows = [row.text.split("\n") for row in table_rows]

        data = {}

        for key, value in rows:
            key = table_key_cleaner(key)
            data[key] = value

        return data

    else:
        return None


class SummaryPageNotFound(AttributeError):
    pass


def get_summary_page(
    symbol: str, fuzzy_search=True, raise_error=False, session=None, proxies=None, timeout=5
):

    if fuzzy_search:
        fuzzy_data = fuzzy_symbol_seach(symbol, session=session, first=True)

        if fuzzy_data:
            symbol = fuzzy_data.symbol

    url = f"https://finance.yahoo.com/quote/{symbol}?p={symbol}"

    if session:
        response = session.get(url, proxies=proxies, timeout=timeout)
    else:
        response = requests.get(url, proxies=proxies, timeout=timeout)

    if response.ok:

        html = HTML(html=response.text, url=url)

        header_page_data = parse_header(html)

        summary_page_data = parse_summary_table(html)

        if header_page_data and summary_page_data:

            data = ChainMap(header_page_data, summary_page_data)
            data["symbol"] = symbol

            return Summary(**data)

    if raise_error:
        raise SummaryPageNotFound(f"{symbol} summary page not found.")
    else:
        return None


def get_summary_pages(
    symbols: List[str],
    fuzzy_search=True,
    raise_error=False,
    with_threads=False,
    thread_count=5,
    session=None,
    progress_bar=True,
    proxies=None,
    timeout=5,
):

    symbols = list(set(symbols))
    data = []

    if with_threads:
        from concurrent.futures import as_completed, ThreadPoolExecutor

        if fuzzy_search:
            valid_symbols = []

            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                futures = [
                    executor.submit(
                        fuzzy_symbol_seach,
                        symbol,
                        first=True,
                        session=session,
                        proxies=proxies,
                        timeout=timeout,
                    )
                    for symbol in symbols
                ]

                pbar = enlighten.Counter(
                    total=len(futures), desc="Validating symbols...", unit="symbols"
                )

                for future in as_completed(futures):
                    valid_symbols.append(future.result())
                    if progress_bar:
                        pbar.update()

            valid_symbols = filter(lambda s: s is not None, valid_symbols)
            symbols = list(set([s.symbol for s in valid_symbols]))

        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = [
                executor.submit(
                    get_summary_page,
                    symbol,
                    fuzzy_search=False,
                    raise_error=raise_error,
                    session=session,
                    proxies=proxies,
                    timeout=timeout,
                )
                for symbol in symbols
            ]

            pbar = enlighten.Counter(
                total=len(futures), desc="Downloading Summary Data...", unit="symbols"
            )
            for future in as_completed(futures):
                results = future.result()
                if results:
                    data.append(results)
                if progress_bar:
                    pbar.update()

    else:

        if fuzzy_search:
            valid_symbols = []

            pbar = enlighten.Counter(
                total=len(symbols), desc="Validating symbols...", unit="symbols"
            )
            for symbol in symbols:
                result = fuzzy_symbol_seach(
                    symbol, first=True, session=session, proxies=proxies, timeout=timeout
                )
                valid_symbols.append(result)
                if progress_bar:
                    pbar.update()

            valid_symbols = filter(lambda s: s is not None, valid_symbols)
            symbols = list(set([s.symbol for s in valid_symbols]))

        pbar = enlighten.Counter(
            total=len(symbols), desc="Downloading Summary Data...", unit="symbols"
        )
        for symbol in symbols:
            results = get_summary_page(
                symbol,
                fuzzy_search=False,
                raise_error=raise_error,
                session=session,
                proxies=proxies,
                timeout=timeout,
            )

            if results:
                data.append(results)
            if progress_bar:
                pbar.update()

    if data:
        return SummaryGroup(data=data)

    else:
        return None
